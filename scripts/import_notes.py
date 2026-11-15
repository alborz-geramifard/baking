#!/usr/bin/env python3
"""Import baking recipes into recipes.js for the Baking Book page.

Two sources are supported:

  1. Straight from the Apple Notes app (macOS):
       python3 scripts/import_notes.py --list-folders
       python3 scripts/import_notes.py --notes-folder "Baking"
     The first run asks macOS for permission to let Terminal control Notes; click OK.

  2. A directory of exported notes (.html, .htm, .txt or .md files), e.g. from
     Notes' File > Export, or a tool such as "Exporter" from the App Store:
       python3 scripts/import_notes.py --dir ~/Desktop/BakingNotes

Each note's text is kept exactly as written (formatting, line breaks, lists),
so the page shows the instructions the same way they appear in Notes.
"""
import argparse
import html
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "recipes.js"

JXA_LIST = r"""
function run() {
  const Notes = Application('Notes');
  const out = [];
  Notes.accounts().forEach(acc => acc.folders().forEach(f => {
    out.push(acc.name() + ' / ' + f.name() + '  (' + f.notes().length + ' notes)');
  }));
  return out.join('\n');
}
"""

JXA_EXPORT = r"""
function run(argv) {
  const wanted = argv[0];
  const Notes = Application('Notes');
  const out = [];
  Notes.accounts().forEach(acc => acc.folders().forEach(f => {
    if (f.name() !== wanted) return;
    f.notes().forEach(n => {
      out.push({
        title: n.name(),
        body: n.body(),
        created: n.creationDate().toISOString(),
        modified: n.modificationDate().toISOString(),
      });
    });
  }));
  return JSON.stringify(out);
}
"""


def osascript(script, *args):
    res = subprocess.run(["osascript", "-l", "JavaScript", "-e", script, *args],
                         capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit("Could not read Apple Notes:\n" + res.stderr.strip() +
                 "\n(Check System Settings > Privacy & Security > Automation and allow your terminal to control Notes.)")
    return res.stdout.strip()


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def drop_title_line(body, title):
    """Apple Notes puts the note's title as the first line of the body; the page shows it as a heading already."""
    m = re.match(r"\s*<(div|h1|h2|h3|p)\b[^>]*>(.*?)</\1>\s*", body, re.S | re.I)
    if m and strip_tags(m.group(2)) == title.strip():
        body = body[m.end():]
        body = re.sub(r"^\s*<div>\s*<br\s*/?>\s*</div>\s*", "", body, flags=re.I)  # blank line after title
    return body


def slugify(s, taken):
    base = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "recipe"
    slug, i = base, 2
    while slug in taken:
        slug, i = f"{base}-{i}", i + 1
    taken.add(slug)
    return slug


def from_notes(folder):
    raw = json.loads(osascript(JXA_EXPORT, folder) or "[]")
    if not raw:
        sys.exit(f'No notes found in a folder named "{folder}". Run with --list-folders to see folder names.')
    return [{"title": n["title"].strip(), "body": drop_title_line(n["body"], n["title"]),
             "created": n["created"][:10], "modified": n["modified"][:10]} for n in raw]


def from_dir(path):
    path = Path(path).expanduser()
    if not path.is_dir():
        sys.exit(f"Not a directory: {path}")
    recipes = []
    for f in sorted(path.rglob("*")):
        ext = f.suffix.lower()
        if ext not in {".html", ".htm", ".txt", ".md"}:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        title = f.stem
        if ext in {".html", ".htm"}:
            t = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
            if t and strip_tags(t.group(1)):
                title = strip_tags(t.group(1))
            b = re.search(r"<body[^>]*>(.*)</body>", text, re.S | re.I)
            body = b.group(1) if b else text
            body = drop_title_line(body, title)
        else:
            lines = text.replace("\r\n", "\n").split("\n")
            first = lines[0].lstrip("# ").strip() if lines else ""
            if first:
                title = first
                lines = lines[1:]
                while lines and not lines[0].strip():
                    lines = lines[1:]
            body = "\n".join(lines).rstrip()  # plain text: shown with its line breaks untouched
        st = f.stat()
        recipes.append({"title": title, "body": body,
                        "created": date.fromtimestamp(getattr(st, "st_birthtime", st.st_mtime)).isoformat(),
                        "modified": date.fromtimestamp(st.st_mtime).isoformat()})
    if not recipes:
        sys.exit(f"No .html/.htm/.txt/.md files found in {path}")
    return recipes


def write(recipes, out):
    taken = set()
    recipes.sort(key=lambda r: r["title"].lower())
    data = [{"id": slugify(r["title"], taken), **r} for r in recipes]
    out.write_text("// Generated by scripts/import_notes.py. Re-run the script to refresh.\n"
                   "window.RECIPES = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
                   encoding="utf-8")
    print(f"Wrote {len(data)} recipes to {out}")
    for r in data:
        print("  •", r["title"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--notes-folder", help="name of the Apple Notes folder holding your recipes")
    src.add_argument("--dir", help="directory of exported notes (.html/.txt/.md)")
    src.add_argument("--list-folders", action="store_true", help="list Apple Notes folders and exit")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output file (default: {DEFAULT_OUT.name})")
    a = ap.parse_args()
    if a.list_folders:
        print(osascript(JXA_LIST))
        return
    write(from_notes(a.notes_folder) if a.notes_folder else from_dir(a.dir), a.out)


if __name__ == "__main__":
    main()
