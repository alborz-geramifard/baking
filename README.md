# Baking with Alborz

A one-page showcase of my baking recipes. Open `index.html` in a browser. Click a cake to open its recipe.

Below it, every recipe is laid out the same way as a **bake-along checklist**: **Ingredients**, then **Instructions**, then **Tips** (when the note has any). A recipe made in several parts (sponge, mousse, glaze…) gets one box per part, **Stage A, B, C…**, with its steps numbered 1, 2, 3 inside each stage. Every ingredient and step is a box you can tick off as you go. Ticks are saved only in your own browser, so they never affect anyone else, and **Reset** clears them for that recipe. **Focus mode** fills the screen with just the next step, in big type. Tap the step (or **Done**) when it's finished: it gets ticked and the next unticked step slides in, with a peek at what's coming up. **Back** (or ←) revisits earlier steps, → also moves on, and Esc or ✕ returns to the full recipe. Where the browser allows it, the screen stays awake while Focus mode is open. The layout is read from each note's headings (Ingredients, Steps, Tips, or part names like "Cookie Layer") and from how its lines read, so a note with clear headings comes out best. Only a note that can't be read this way is shown as written instead. Recipe pages have no previous/next links; **All bakes** goes back to the list.

Persian bakes show an English name with the Farsi name after it, in a Farsi font: **Walnut Cookies (شیرینی گردویی)** and **Coconut Cookies (شیرینی نارگیلی)**. The names are set in the `NAMES` list near the top of the script in `index.html` (keyed by the note's title, so they survive re-importing); add a line there for any new Persian recipe. Searching works with either name.

Each cake carries four pills and no others: its total time, rounded to whole hours (**13 Hrs**, or **1 Hr**; the exact time is in the At a glance panel), its layer count, how many ingredients, and its size, taken out of the title ("Chocolate Banana - 8 Inch Round" shows as **Chocolate Banana** with an **8" round** pill; "(8x)" → **Makes 8** works the same way; a cake whose title gives no size gets an **8" round** pill, since that is the pan these cakes are made in, except bundt, square and mold cakes, which use other pans: give one of those a `size` field in `recipes.js`, in inches, to show its pan, as the Entreme Mold Cake does with `"size": "6×6 inch square"` for its 15 cm square insert, shown as **6×6" square**; the importer keeps it). Oven temperature and dates are not pills: the temperature is in the At a glance panel and the date is at the foot of the recipe. The layer count comes from the recipe, not the title: every layer you see in a slice once the sponge is cut, so a sponge sliced into 2 or 3 with mousse between gives a range like **3–5 layers** (mousse, cream, crunch and ganache count; mirror glazes, syrups and decorations don't). It is the `layers` field in `recipes.js` (`min`, `max` and `stack`, the layers listed out, shown under the pills on the recipe page); the importer keeps it, like descriptions.

**Credits.** Recipes adapted from someone else's (like the Flour Mousse Cake, my interpretation of Joanne Chang's cake from Flour Bakery + Café) say so on the recipe page, not on the card in the list: the recipe page has a **With credit to** panel linking each source, with its icon. To credit a recipe, add a `credits` list to it in `recipes.js`, e.g. `"credits": [{"name": "Flour Bakery + Café", "url": "https://flourbakery.com/", "icon": "images/sources/flour-bakery.svg", "note": "From her cookbook Flour, Too"}]`. Put source icons in `images/sources/` (the importer never touches that folder). Credits, like descriptions, are kept when the importer is re-run.

**Links.** Web addresses are never shown raw. A note line that is only an address (such as "Link: https://…") appears as the tip "See more details about the steps here", with "here" as the hyperlink; an address inside a sentence shows as its site name.

Each recipe page opens with an **At a glance** panel: oven temperature, an estimate of the total time from start to serving (how long it's in the oven, plus the cooling, chilling, freezing and resting the recipe asks for, plus some hands-on time, with a bare "overnight" counted as 8 hours), shown once, as **total to prepare**, with its parts listed under it (**manual work**, **cooking** in the oven, and **cooling & chilling**) and drawn as a ring in matching colours, how many ingredients, and a bar showing what goes in by weight (ml counted as grams, an egg as about 50 g). Each part of the bar shows its ingredient name and share inside it when there's room; parts too small for that get their label just outside the bar, joined to the part by a line in the same colour. The ingredient count and the times are checked by hand for each recipe and kept in its `glance` field in `recipes.js`: `ingredients` (how many different ingredients, each counted once even when several parts use it), `hands` (minutes of manual work, an estimate) and `cook` and `wait`, each a list of `[step, minutes]` (a range counts at its middle, "at least 6 hours, preferably overnight" as 6 hours, a bare "overnight" as 8 hours, and "let it cool" with no time gets an estimate). The page adds these up, so the total is always exactly its three parts, and **How it adds up** under the total lists every step behind them. The importer keeps `glance`, like descriptions, so re-check it when a recipe's note changes. A recipe without one gets both numbers estimated from the note's text. The oven temperature and the weight bar are always read from the note. The recipe below them is still shown exactly as written. Each recipe is shown with its own photo: the first picture in the note. A recipe without a photo, or whose photo won't load, gets a drawn cake instead, made from the recipe name: loaves, bundts, cheesecakes and layer cakes get their own shapes, and flavours like chocolate, lemon or carrot pick the colours.

The banner shows an anime-style illustration of me as a baker (`images/baker-portrait.webp`), generated with ChatGPT from my profile photo. It's a full-bleed 1024×1024 square; the page crops it to a circle, so keep the face and hat inside the middle. To swap it, replace that file with another square image. If the file is missing, the portrait is simply hidden.

**Movement.** The page is meant to feel alive without getting in the way. The title's letters spring in one by one (hover a letter and it hops), the banner's bottom edge runs down onto the page like icing, cards rise and settle as you scroll to them, and searching or sorting makes the cards glide to their new places. The featured cake waits while you hover it, and a thin line under it shows when the next one is due. On a recipe, ticking a step throws a few sprinkles, and finishing every step showers the page with them (in Focus mode too). All of it is switched off for anyone whose device asks for reduced motion, and none of it appears in print. It lives in the "Motion layer 2" blocks of `index.html` (one in the styles, one in the script).

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

Each note's title becomes the recipe's name. To publish a note under a better name without renaming the note itself, add it to `TITLE_RENAMES` in the script ("New 5 layer cake" is shown as **Chocolate Hazelnut Coconut Mousse Cake (5 Layers)**). Links that used the old name keep working. The rest of the note is shown as written, keeping its line breaks, bold and italic text, lists and tables. The one change: measurements are written the same way in every recipe. After a number, tablespoons become **tbsp**, teaspoons **tsp**, grams (gr, grams) **g**, plus **kg** and **ml**, always with a space ("1 Tbsp" → "1 tbsp", "75 Gr" → "75 g", "100g" → "100 g"). Words without a number, like "a teaspoon of water", are left alone. This is `standardize_units` in the script.

### Pictures

Pictures in a note are saved as web-sized JPEGs in `images/recipes/` (for example `images/recipes/banana-cake.jpg`), and the first one becomes the recipe's photo on its card and at the top of its page. The importer clears that folder on each run, so don't keep other files there. The script lists any recipe that has no photo.

This works with both `--notes-folder` (Apple Notes hands the pictures over inside the note) and `--dir`, if the export saved the notes as HTML with their pictures. The script finds pictures embedded in the HTML or saved next to the `.html` files. It can't read PDFs, so Notes' **File › Export as PDF** won't work here.

A few notes in the folder are always skipped (see `DEFAULT_EXCLUDE` in the script). To leave out more, add `--exclude` with part of the title, as many times as you need:

```sh
python3 scripts/import_notes.py --notes-folder "iCloud / Dessert" --exclude "Trip" --exclude "Shopping list"
```
