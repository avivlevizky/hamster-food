# Frontmatter schema

Every file under `recipes/` starts with YAML frontmatter. Unknown keys are not allowed —
if something needs a new field, add it here first.

| key | type | required | notes |
|---|---|---|---|
| `title` | string | yes | The dish's own name, in its own language (`Panini di Semola all'Olio`) |
| `title_he` | string | yes | Hebrew name as the user would say it |
| `cuisine` | enum | yes | `italian` `israeli` `french` `levantine` `japanese` `other` |
| `region` | string | no | `puglia`, `toscana`, `sicilia` — only when the dish is regional |
| `type` | enum | yes | `bread` `pasta` `main` `side` `sauce` `dessert` `preserve` `basic` |
| `leavening` | enum | no | bread only: `sourdough` `yeast` `mixed` `none` |
| `yield` | map | yes | `{count: 8, unit: roll}` or `{servings: 2}` |
| `total_time_h` | number | yes | Wall-clock including fermentation and resting, not active time |
| `active_time_min` | number | no | Hands-on minutes |
| `hydration_pct` | number | no | Bread only. Total water / total flour, starter included |
| `difficulty` | enum | yes | `easy` `medium` `hard` |
| `status` | enum | yes | `untested` `tested` `favorite` — only the user promotes |
| `tags` | list | no | lowercase kebab-case, free-form |
| `sources` | list of maps | yes | `{name, url, credential, contributed}` |
| `submitted_by` | string | no | Who sent it in, when the recipe arrived from a person rather than a page |
| `updated` | date | yes | `YYYY-MM-DD` |

## status

- `untested` — written up, never cooked. The default for anything ported or researched.
- `tested` — cooked at least once, works.
- `favorite` — in the regular rotation.

The distinction is the single most useful field in the archive a year from now. Never set
it on the user's behalf.

## yield

Use `count` + `unit` for discrete items (rolls, buns, jars) and add `unit_weight_g` when
the item has a target weight. Use `servings` for plated dishes.

## sources

```yaml
sources:
  - name: Biancolievito
    url: https://biancolievito.it/en/semolina-bread-with-sourdoough/
    credential: Italian professional baking site
    contributed: Two-stage bake temperature and the steam method
```

When the source is a person and not a page, omit `url` and put what they are in
`credential` — `סבתא של דנה`, `שף במסעדה בחיפה`. A recipe that came in by mail still
needs a sources entry; the sender is the source.

`contributed` is what makes the list useful — without it nobody can tell which source to
re-read when something goes wrong.
