# Bakery with Alborz

A one-page showcase of my baking recipes. Open `index.html` in a browser. Click a recipe to see it exactly as written.

Below it, every recipe is laid out the same way as a **bake-along checklist**: **Ingredients**, then **Instructions**, then **Tips** (when the note has any). A recipe made in several parts (sponge, mousse, glaze…) gets one box per part, **Stage A, B, C…**, with its steps numbered 1, 2, 3 inside each stage. Every ingredient and step is a box you can tick off as you go. Ticks are saved only in your own browser, so they never affect anyone else, and **Reset** clears them for that recipe. The layout is read from each note's headings (Ingredients, Steps, Tips, or part names like "Cookie Layer") and from how its lines read, so a note with clear headings comes out best. The original note is still there under **Show the note as written**.

Each recipe page opens with an **At a glance** panel: oven temperature, bake time, how many ingredients, and a bar showing what goes in by weight (ml counted as grams, an egg as about 50 g). These are read from the note's text. The recipe below them is still shown exactly as written. Each recipe is shown with its own photo: the first picture in the note. A recipe without a photo, or whose photo won't load, gets a drawn cake instead, made from the recipe name: loaves, bundts, cheesecakes and layer cakes get their own shapes, and flavours like chocolate, lemon or carrot pick the colours.

The banner shows an anime-style illustration of me as a baker (`images/baker-portrait.webp`), generated with ChatGPT from my profile photo. It's a full-bleed 1024×1024 square; the page crops it to a circle, so keep the face and hat inside the middle. To swap it, replace that file with another square image. If the file is missing, the portrait is simply hidden.

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

You can give the folder exactly as `--list-folders` prints it, account included, e.g. `--notes-folder "iCloud / Dessert"`. Names with spaces work with or without quotes.

The first run asks macOS to let your terminal control Notes. Click **OK**.

If you'd rather export the notes yourself (File › Export, or an exporter app), point the script at that folder instead. It reads `.html`, `.htm`, `.txt` and `.md` files:

```sh
python3 scripts/import_notes.py --dir ~/Desktop/BakingNotes
```

Paths with spaces are fine. `--dir "iCloud / Dessert"` is read as the Dessert folder in iCloud Drive.

Each note's title becomes the recipe's name. The rest of the note is shown as written, keeping its line breaks, bold and italic text, lists and tables. The one change: measurements are written the same way in every recipe. After a number, tablespoons become **tbsp**, teaspoons **tsp**, grams (gr, grams) **g**, plus **kg** and **ml**, always with a space ("1 Tbsp" → "1 tbsp", "75 Gr" → "75 g", "100g" → "100 g"). Words without a number, like "a teaspoon of water", are left alone. This is `standardize_units` in the script.

### Pictures

Pictures in a note are saved as web-sized JPEGs in `images/recipes/` (for example `images/recipes/banana-cake.jpg`), and the first one becomes the recipe's photo on its card and at the top of its page. The importer clears that folder on each run, so don't keep other files there. The script lists any recipe that has no photo.

This works with both `--notes-folder` (Apple Notes hands the pictures over inside the note) and `--dir`, if the export saved the notes as HTML with their pictures. The script finds pictures embedded in the HTML or saved next to the `.html` files. It can't read PDFs, so Notes' **File › Export as PDF** won't work here.

A few notes in the folder are always skipped (see `DEFAULT_EXCLUDE` in the script). To leave out more, add `--exclude` with part of the title, as many times as you need:

```sh
python3 scripts/import_notes.py --notes-folder "iCloud / Dessert" --exclude "Trip" --exclude "Shopping list"
```
