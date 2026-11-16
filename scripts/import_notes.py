#!/usr/bin/env python3
"""Import baking recipes into recipes.js for the Baking Book page.

Two sources are supported:

  1. Straight from the Apple Notes app (macOS):
       python3 scripts/import_notes.py --list-folders
       python3 scripts/import_notes.py --notes-folder "Baking"
       python3 scripts/import_notes.py --notes-folder "iCloud / Dessert"
     A folder can be given by name alone or as "Account / Folder", exactly as
     --list-folders prints it. Spaces are fine, quoted or not.
     The first run asks macOS for permission to let Terminal control Notes; click OK.

  2. A directory of exported notes (.html, .htm, .txt or .md files), e.g. from
     Notes' File > Export, or a tool such as "Exporter" from the App Store:
       python3 scripts/import_notes.py --dir ~/Desktop/BakingNotes

Each note's text is kept exactly as written (formatting, line breaks, lists),
so the page shows the instructions the same way they appear in Notes.

Pictures in a note are saved as JPEGs in images/recipes/ and the first one
becomes the cake's photo. Notes that aren't recipes can be left out with
--exclude "part of the title" (repeatable), on top of DEFAULT_EXCLUDE below.
"""
import argparse
import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "recipes.js"
# Notes kept in the recipe folder that shouldn't be published (non-recipes and removed recipes);
# always skipped. Whole title, ignoring case, punctuation/dash style and extra spaces.
DEFAULT_EXCLUDE = [
    "Dessert Tricks", "Opera Cake - Louise Lindberg",
    # Not recipes: personal notes that live in the same Notes folder.
    "Australia Trip", "Less shakiness on videos (up down, left, right)",
]


def title_key(title):
    return " ".join(re.sub(r"[\W_]+", " ", title.lower()).split())


EXTRA_EXCLUDE = []  # filled from --exclude: leave out notes whose title contains any of these


def is_recipe(title):
    key = title_key(title)
    if key in {title_key(t) for t in DEFAULT_EXCLUDE} or any(title_key(x) in key for x in EXTRA_EXCLUDE if title_key(x)):
        print(f"Skipped (excluded): {title.strip()}")
        return False
    return True

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
  const norm = s => String(s).replace(/\s+/g, ' ').trim().toLowerCase();
  const wantAcc = norm(argv[0] || '');
  const wantFolder = norm(argv[1] || '');
  const Notes = Application('Notes');
  const out = [];
  Notes.accounts().forEach(acc => acc.folders().forEach(f => {
    if (norm(f.name()) !== wantFolder) return;
    if (wantAcc && norm(acc.name()) !== wantAcc) return;
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


EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]")


def clean_title(title):
    """Note titles often start with an emoji (e.g. "🎂Walnut Cake"); the page shows plain names."""
    return " ".join(EMOJI_RE.sub(" ", title).split())


def slugify(s, taken):
    base = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "recipe"
    slug, i = base, 2
    while slug in taken:
        slug, i = f"{base}-{i}", i + 1
    taken.add(slug)
    return slug


def parse_folder(spec):
    """Turn what the user typed into (account, folder).

    Accepts "Dessert", "iCloud / Dessert" or "iCloud/Dessert", and also a line
    pasted straight from --list-folders, e.g. "iCloud / Dessert  (12 notes)".
    Returns account "" when no account was given (match the folder in any account).
    """
    spec = re.sub(r"\s*\(\d+ notes?\)\s*$", "", spec)
    spec = re.sub(r"\s+", " ", spec).strip()
    if "/" in spec:
        acc, folder = spec.split("/", 1)
        return acc.strip(), folder.strip()
    return "", spec


def from_notes(spec):
    account, folder = parse_folder(spec)
    raw = json.loads(osascript(JXA_EXPORT, account, folder) or "[]")
    if not raw and account:
        # Maybe the folder's own name contains a "/": try the whole thing as a folder name.
        raw = json.loads(osascript(JXA_EXPORT, "", re.sub(r"\s+", " ", spec).strip()) or "[]")
    if not raw:
        where = f'"{folder}" in account "{account}"' if account else f'"{folder}"'
        sys.exit(f"No notes found in a folder named {where}. Folders available:\n" + osascript(JXA_LIST))
    return [{"title": n["title"].strip(), "body": drop_title_line(n["body"], n["title"]),
             "created": n["created"][:10], "modified": n["modified"][:10]}
            for n in raw if is_recipe(n["title"])]


ICLOUD_DRIVE = Path("~/Library/Mobile Documents/com~apple~CloudDocs").expanduser()


def resolve_dir(spec):
    """Find the export folder, allowing spaces and a few shorthands.

    "iCloud / Dessert" or "iCloud Drive/Dessert" is taken to mean the Dessert
    folder in iCloud Drive (~/Library/Mobile Documents/com~apple~CloudDocs).
    """
    path = Path(spec.strip()).expanduser()
    if path.is_dir():
        return path
    m = re.match(r"\s*iCloud(?:\s+Drive)?\s*/\s*(.*)$", spec, re.I)
    if m:
        rest = "/".join(part.strip() for part in m.group(1).split("/"))
        cand = ICLOUD_DRIVE / rest
        if cand.is_dir():
            return cand
    sys.exit(f"Not a directory: {path}\n(If the path has spaces, put it in quotes, "
             f'e.g. --dir "~/Library/Mobile Documents/com~apple~CloudDocs/Dessert".)')


def from_dir(spec):
    path = resolve_dir(spec)
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
        if not is_recipe(title):
            continue
        st = f.stat()
        recipes.append({"title": title, "body": body, "base": f.parent,
                        "created": date.fromtimestamp(getattr(st, "st_birthtime", st.st_mtime)).isoformat(),
                        "modified": date.fromtimestamp(st.st_mtime).isoformat()})
    if not recipes:
        sys.exit(f"No .html/.htm/.txt/.md files found in {path}")
    return recipes


def existing_descriptions(out):
    """Card descriptions already written in recipes.js, keyed by lower-cased title.

    Notes don't carry a description, so re-importing keeps the ones written by hand."""
    try:
        text = out.read_text(encoding="utf-8")
        start, end = text.index("["), text.rindex("]") + 1
        return {clean_title(str(r.get("title", ""))).lower(): r["description"]
                for r in json.loads(text[start:end]) if r.get("description")}
    except (OSError, ValueError, TypeError, AttributeError):
        return {}


IMG_RE = re.compile(r"""(<img\b[^>]*?\ssrc\s*=\s*)(["'])(.*?)\2""", re.I | re.S)
DATA_RE = re.compile(r"data:image/([\w.+-]+);base64,(.*)", re.I | re.S)
PHOTO_MAX = 1200  # longest side, in pixels, of the photos saved for the page


def save_photo(raw, ext, dest_stem):
    """Write one picture next to the page, as a web-sized JPEG when macOS `sips` is available.

    Notes keeps photos as multi-megabyte PNG/HEIC; browsers can't show HEIC and the page
    would be slow with the originals. Without sips the original bytes are kept as they are.
    Returns the file written.
    """
    ext = {"jpeg": "jpg", "svg+xml": "svg"}.get(ext.lower(), ext.lower())
    if shutil.which("sips") and ext not in {"gif", "svg"}:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / f"in.{ext}"
            src.write_bytes(raw)
            dest = dest_stem.with_suffix(".jpg")
            res = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                                  "-Z", str(PHOTO_MAX), str(src), "--out", str(dest)],
                                 capture_output=True, text=True)
            if res.returncode == 0 and dest.exists():
                return dest
    dest = dest_stem.with_suffix("." + ext)
    dest.write_bytes(raw)
    return dest


def extract_photos(r, slug, img_dir, page_dir):
    """Move the note's pictures out of the HTML into image files and point the note at them.

    Embedded pictures (data: URIs from Apple Notes) and pictures next to an exported note
    are saved as images/recipes/<slug>.jpg, <slug>-2.jpg, ...; web links are left as they are.
    The first picture becomes the recipe's "image", shown on its card and at the top of its page.
    """
    found, saved = [], [0]

    def swap(m):
        src = html.unescape(m.group(3)).strip()
        raw = ext = None
        d = DATA_RE.match(src)
        if d:
            try:
                raw, ext = base64.b64decode(re.sub(r"\s+", "", d.group(2))), d.group(1)
            except ValueError:
                return m.group(0)
        elif re.match(r"https?:", src, re.I):
            found.append(src)
            return m.group(0)
        elif r.get("base") and not re.match(r"[a-z][\w+.-]*:", src, re.I):
            f = (Path(r["base"]) / unquote(src.split("?")[0])).resolve()
            if f.is_file():
                raw, ext = f.read_bytes(), f.suffix.lstrip(".") or "jpg"
        if raw is None:
            return m.group(0)
        saved[0] += 1
        n = saved[0]
        dest = save_photo(raw, ext, img_dir / (slug if n == 1 else f"{slug}-{n}"))
        rel = os.path.relpath(dest, page_dir).replace(os.sep, "/")
        found.append(rel)
        return f"{m.group(1)}{m.group(2)}{html.escape(rel)}{m.group(2)}"

    r["body"] = IMG_RE.sub(swap, r["body"])
    if found:
        r["image"] = found[0]


def write(recipes, out):
    taken = set()
    for r in recipes:
        r["title"] = clean_title(r["title"])
    recipes.sort(key=lambda r: r["title"].lower())
    kept = existing_descriptions(out)
    data = []
    for r in recipes:
        item = {"id": slugify(r["title"], taken), "title": r["title"]}
        desc = kept.get(r["title"].strip().lower())
        if desc:
            item["description"] = desc
        item.update(r)
        data.append(item)
    page_dir = out.resolve().parent
    img_dir = page_dir / "images" / "recipes"
    if img_dir.is_dir():  # this folder belongs to the importer: start fresh so removed notes leave no photos behind
        shutil.rmtree(img_dir)
    img_dir.mkdir(parents=True, exist_ok=True)
    for r in data:
        extract_photos(r, r["id"], img_dir, page_dir)
        r.pop("base", None)
    out.write_text("// Generated by scripts/import_notes.py. Re-run the script to refresh.\n"
                   "// Add a \"description\" to any recipe for its card blurb (about the cake, not its ingredients);\n"
                   "// descriptions are kept when the script is re-run.\n"
                   "window.RECIPES = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
                   encoding="utf-8")
    print(f"Wrote {len(data)} recipes to {out}")
    for r in data:
        print("  •", r["title"], "" if r.get("image") else "(no photo: a drawn cake is shown instead)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    # nargs="+" so an unquoted name with spaces (e.g. iCloud / Dessert) still arrives as one value.
    src.add_argument("--notes-folder", nargs="+", metavar="FOLDER",
                     help='Apple Notes folder holding your recipes, e.g. "Baking" or "iCloud / Dessert"')
    src.add_argument("--dir", nargs="+", metavar="PATH",
                     help="directory of exported notes (.html/.txt/.md); spaces are fine")
    src.add_argument("--list-folders", action="store_true", help="list Apple Notes folders and exit")
    ap.add_argument("--exclude", action="append", default=[], metavar="TITLE",
                    help='leave out notes whose title contains this text (repeatable), e.g. --exclude "Trip"')
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output file (default: {DEFAULT_OUT.name})")
    a = ap.parse_args()
    EXTRA_EXCLUDE.extend(a.exclude)
    if a.list_folders:
        print(osascript(JXA_LIST))
        return
    if a.notes_folder:
        recipes = from_notes(" ".join(a.notes_folder))
    else:
        recipes = from_dir(" ".join(a.dir))
    write(recipes, a.out)


if __name__ == "__main__":
    main()
