// Recipe data for the Baking Book page.
//
// THESE ARE PLACEHOLDER SAMPLES. Replace them with your own recipes by running:
//   python3 scripts/import_notes.py --notes-folder "Baking"     (straight from Apple Notes)
//   python3 scripts/import_notes.py --dir ~/Desktop/BakingNotes (from a folder of exported notes)
//
// Each recipe: { id, title, description (short card blurb about the cake, not its ingredients), body (HTML from the note, rendered as written), created, modified, sample }
window.RECIPES = [
  {
    "id": "brown-butter-olive-oil-cake",
    "title": "Brown Butter Olive Oil Cake",
    "description": "A tender, golden everyday cake with a bright citrus lift. Even better the day after baking.",
    "sample": true,
    "created": "2026-03-02",
    "modified": "2026-03-02",
    "body": "<div><b>Ingredients</b></div><ul><li>115 g butter, browned and cooled</li><li>120 ml good olive oil</li><li>200 g sugar</li><li>3 eggs, room temp</li><li>zest of 1 orange</li><li>240 g flour</li><li>1½ tsp baking powder</li><li>½ tsp salt</li><li>180 ml whole milk</li></ul><div><br></div><div><b>Method</b></div><ol><li>Oven 175°C. Line a 9\" round.</li><li>Rub zest into sugar with fingers until it smells like oranges.</li><li>Whisk in eggs until pale, ~2 min. Stream in butter + oil.</li><li>Fold in dry ingredients alternately with milk (dry, milk, dry, milk, dry).</li><li>Bake 40–45 min. Cool 15 min in the pan.</li></ol><div><br></div><div><i>Note: even better on day two.</i></div>"
  },
  {
    "id": "lemon-ricotta-loaf",
    "title": "Lemon Ricotta Loaf",
    "description": "A soft, sunny loaf with a sweet-tart glaze, made for an afternoon cup of tea.",
    "sample": true,
    "created": "2026-04-11",
    "modified": "2026-05-01",
    "body": "<div>Makes 1 loaf (9x5)</div><div><br></div><div><b>Dry</b></div><div>190 g flour</div><div>2 tsp baking powder</div><div>¼ tsp salt</div><div><br></div><div><b>Wet</b></div><div>240 g whole milk ricotta</div><div>200 g sugar + zest of 2 lemons</div><div>3 eggs</div><div>115 g melted butter</div><div><br></div><div>Mix wet. Fold in dry — don't overmix!!</div><div>Bake 175°C for 50–55 min, toothpick clean.</div><div><br></div><div><b>Glaze:</b> 120 g icing sugar + 2 tbsp lemon juice. Pour on while slightly warm.</div>"
  },
  {
    "id": "chocolate-sour-cream-cake",
    "title": "Chocolate Sour Cream Cake",
    "description": "Dark, fudgy layers under a cloud of whipped ganache. The birthday cake.",
    "sample": true,
    "created": "2026-01-20",
    "modified": "2026-02-14",
    "body": "<div><b>Cake</b></div><ul><li>225 g flour</li><li>350 g sugar</li><li>85 g cocoa (dutch)</li><li>2 tsp bicarb</li><li>1 tsp salt</li><li>2 eggs</li><li>240 ml sour cream</li><li>120 ml oil</li><li>240 ml hot coffee</li></ul><div><br></div><div><b>Steps</b></div><ol><li>180°C, two 8\" pans.</li><li>Whisk dry. Add eggs, sour cream, oil.</li><li>Pour in hot coffee last — batter will be thin, that's right.</li><li>30–35 min.</li></ol><div><br></div><div><b>Frosting</b></div><div>Ganache: 300 g dark choc + 300 ml cream. Whip once cool.</div>"
  },
  {
    "id": "carrot-cake",
    "title": "Carrot Cake",
    "description": "A warmly spiced, cosy sheet cake with a little crunch and a thick, tangy frosting.",
    "sample": true,
    "created": "2025-11-02",
    "modified": "2026-04-03",
    "body": "<div><b>Ingredients</b></div><ul><li>300 g grated carrot</li><li>250 g flour</li><li>2 tsp cinnamon, ½ tsp nutmeg, ¼ tsp ginger</li><li>1½ tsp baking soda</li><li>4 eggs</li><li>200 g brown sugar + 100 g white</li><li>240 ml oil</li><li>100 g toasted walnuts</li></ul><div><br></div><div><b>Method</b></div><ol><li>175°C, 9x13 pan.</li><li>Beat eggs + sugars, stream in oil.</li><li>Fold in dry, then carrots + walnuts.</li><li>35–40 min.</li></ol><div><br></div><div><b>Cream cheese frosting</b></div><div>225 g cream cheese, 115 g butter, 300 g icing sugar, 1 tsp vanilla, pinch salt.</div>"
  },
  {
    "id": "basque-cheesecake",
    "title": "Basque Burnt Cheesecake",
    "description": "Rustic and crustless, with a deeply caramelised top and a creamy, barely-set middle.",
    "sample": true,
    "created": "2026-06-08",
    "modified": "2026-06-08",
    "body": "<div>900 g cream cheese (room temp!)</div><div>300 g sugar</div><div>5 eggs</div><div>480 ml heavy cream</div><div>1 tsp vanilla, ½ tsp salt</div><div>30 g flour</div><div><br></div><div>1. 220°C. Line 10\" springform with 2 crumpled sheets of parchment.</div><div>2. Beat cheese + sugar smooth. Eggs one at a time.</div><div>3. Cream + vanilla, then sift flour over.</div><div>4. Bake 55–65 min. Top very dark, centre very jiggly.</div><div>5. Cool fully. Fridge overnight.</div>"
  }
];
