# AGENTS.md

Read this before touching anything in this repository. It applies to every agent —
Claude, Codex, Cursor, Grok, whatever opened the folder.

## What this is

A personal Hebrew recipe archive, technique-first. Content in Hebrew, structure in English.
Plain Markdown so any tool can read it without a database.

## The rules live in one place

The full working conventions are in `skills/recipe-authoring/SKILL.md`, with details in
`skills/recipe-authoring/references/`. Read the skill before writing or editing a recipe.
Do not restate its rules here — one source of truth.

The short version, if you read nothing else:

- Weights in grams, never cups.
- Every recipe ends with a sources section naming chefs and URLs.
- An ingredient substitution means re-rendering the whole recipe, not a patch.
- `status: untested` until the user says they cooked it. Only the user promotes.
- Hebrew for prose, English for keys and filenames.
- `.github/CODEOWNERS` says who may write where. `scripts/check_owner.py <path>` before writing.

## Layout

```
recipes/<category>/   the recipes themselves
guides/               technique that isn't a dish (starter building, fermentation)
kitchens/<handle>/    each editor's own recipes, owned by them alone
logs/                 bake logs, append-only
templates/            recipe template
skills/               the conventions, as an installable skill
scripts/              build_index.py regenerates INDEX.md
share/                material for non-technical family members
```

## After any change

Run `python scripts/build_index.py`. `INDEX.md` is generated — never hand-edit it.

## Don't

- Don't narrate that you read these files. Apply them and answer.
- Don't invent quantities to fill a template. Missing is better than wrong; ask.
- Don't edit a recipe's numbers to match one bake that went sideways. Log it instead.
