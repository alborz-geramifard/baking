# The Baking Book

A one-page showcase of my baking recipes. Open `index.html` in a browser. Click a cake to see its recipe exactly as written.

## Loading recipes from Apple Notes

```sh
# 1. Find the folder your recipes live in
python3 scripts/import_notes.py --list-folders

# 2. Import it (rewrites recipes.js)
python3 scripts/import_notes.py --notes-folder "Baking"
```

The first run asks macOS to let your terminal control Notes. Click **OK**.

If you'd rather export the notes yourself (File › Export, or an exporter app), point the script at that folder instead. It reads `.html`, `.htm`, `.txt` and `.md` files:

```sh
python3 scripts/import_notes.py --dir ~/Desktop/BakingNotes
```

Each note's title becomes the cake's name. The rest of the note is shown as written, keeping its line breaks, bold and italic text, lists and tables.
