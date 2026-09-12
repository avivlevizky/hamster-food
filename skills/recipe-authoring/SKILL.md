---
name: recipe-authoring
license: MIT
description: >
  Author, edit, scale and port recipes in this repository, in Hebrew, following the house
  format and technique standards. Use this skill whenever the user asks to add a recipe,
  write up a dish, adapt or substitute an ingredient, scale a recipe up or down, convert a
  recipe from a link/video/photo, log a bake, or asks "מה אפשר להכין מ..." / "תוסיף את זה
  למאגר" / "תכתוב לי מתכון". Also use it when reading an existing recipe from this repo
  and answering questions about it, so that answers stay consistent with the recipe's own
  units, ratios and technique notes. Use it even when the request sounds casual — any
  cooking request that touches a file in this repository goes through this skill.
---

# Recipe Authoring

This repository is a personal, technique-first recipe archive. The content language is
Hebrew; the structure, keys and filenames are English so that any tool can parse them.

## Non-negotiables

1. **Weights in grams.** Never cups for flour, sugar, or anything where weight matters.
   Volume is allowed only for liquids under 100 ml and for spoons of seasoning.
2. **Every recipe ends with a sources section.** Name the chef or site and the credential
   when known, with a direct URL, and one line on what that source contributed. A recipe
   with no sources section is not finished.
3. **Substitution means a full re-render.** When an ingredient is swapped, output the
   complete recipe again with every downstream quantity, time and temperature already
   adjusted. Never hand back a delta ("just use 200ml instead") — the whole point is that
   the user can cook from a single screen without reconciling two versions in their head.
4. **Ratios before numbers.** State hydration, salt and fat as percentages of flour weight
   in bread; state sauce-to-pasta ratios in pasta. Absolute amounts go stale when scaling;
   ratios do not.
5. **Say why, briefly.** One clause on the mechanism where it changes the outcome ("cold
   cream off the heat, or the acid splits it"). Not a paragraph of food science.

## Ranking sources

Prefer, in order: credentialed chefs and bakers (Michelin, restaurant, culinary school,
published cookbook) → established institutions (Serious Eats, NYT Cooking, GialloZafferano,
Biancolievito, HaShulchan) → long-running blogs with a track record → social media.
Never lead with AI-generated or untested crowd content. When the user shares a video or a
link, treat it as the primary source and name it as such.

## Writing a new recipe

1. Read `templates/recipe-template.md` and copy it.
2. Fill the frontmatter per `references/schema.md`. Do not invent fields.
3. Filename: English, kebab-case, the dish's own name — `panini-di-semola.md`, not
   `italian-rolls.md`. Place it under `recipes/<category>/`.
4. `status: untested` unless the user says they have actually cooked it. Only the user
   moves a recipe to `tested` or `favorite`. Never promote it on their behalf.
5. Run `python scripts/build_index.py` to regenerate `INDEX.md`.

## Recipes that arrive from other people

Submissions come in by mail (see `share/submit-he.md`) as a link, a photo of a notebook
page, a voice note, or free text. Convert them the same way as anything else, with three
additions:

1. `submitted_by` gets the sender's name, and they go in `sources` — a person is a source
   even without a URL.
2. Missing quantities are asked about, never filled in. Reply to the sender with the
   specific gaps; hold the recipe until they answer rather than shipping a guess.
3. `status: untested` always. A recipe someone else cooks well is still untested *here*.

## Scaling

Scale by the yield field, not by eyeballing. Salt, leavening and spice scale sub-linearly
in practice — when scaling past ~2x, say so and give the adjusted figure rather than the
naive multiple. Pan size and bake time do not scale linearly at all; flag it instead of
silently multiplying.

## Working with the user

- Hebrew for everything the user reads. English only inside frontmatter keys and filenames.
- The user tends to reveal available ingredients progressively. Work with what is on the
  table now rather than asking for a full inventory up front.
- If asked for the same recipe again as plain text, just produce it. No friction, no
  "as I said above".
- Ingredient-constrained requests ("יש לי X ו-Y") are an invitation to propose a real dish,
  not a list of possibilities.

## Bake logs

Bread recipes have a companion log under `logs/`. After a bake, append one row — do not
rewrite history, and do not edit the recipe's own numbers to match a single bake. A recipe
changes only when the user says it should.

## Reference files

- `references/schema.md` — every frontmatter field, its type and allowed values. Read
  before writing or editing frontmatter.
- `references/hebrew-style.md` — terminology, transliteration and unit conventions in
  Hebrew. Read before writing recipe prose.
