# The Baking Book

A one-page showcase of my baking recipes. Open `index.html` in a browser. Click a cake to see its recipe exactly as written.

Each recipe page opens with an **At a glance** panel: oven temperature, bake time, how many ingredients, and a bar showing what goes in by weight (ml counted as grams, an egg as about 50 g). These are read from the note's text. The recipe below them is still shown exactly as written. Each cake picture is drawn from the recipe name: loaves, bundts, cheesecakes and layer cakes get their own shapes, and flavours like chocolate, lemon or carrot pick the colours.

The banner shows an anime-style cartoon of me as a baker (`images/baker-portrait.webp`), generated with ChatGPT from my profile photo. To swap it, replace that file with another square image. If the file is missing, the portrait is simply hidden.

Use the **Share** button (top right of the book, or next to **Print** on a recipe) to pick a platform: WhatsApp, Facebook, X, Pinterest, Reddit, Telegram, Email or Text. You can also copy the link. On phones and in Safari, **More…** opens the device's own share menu. A shared recipe links straight to that recipe. Links only work for other people once the page is online. A `file://` link only opens on your own computer.

## Putting it online (GitHub Pages)

The site is live at **https://alborz-geramifard.com/baking/** (repo: github.com/alborz-geramifard/baking). It is published by the workflow in `.github/workflows/pages.yml`, which runs on every push to `main`.

One-time setup:

```sh
# 1. Create a public repo named "baking" on your account and push this one to it
gh repo create baking --public --source=. --remote=origin --push

# 2. Turn on Pages, deploying with GitHub Actions
gh api -X POST repos/{owner}/baking/pages -f build_type=workflow
```

(Or in the browser: create the repo at github.com/new, push, then **Settings › Pages › Source: GitHub Actions**.)

If the first deploy ran before Pages was turned on, re-run it from the **Actions** tab or with `gh workflow run pages.yml`. After that, every push to `main` updates the site within a minute or two.

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
