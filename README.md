# HamsterFood · מתכונים

ארכיון מתכונים אישי, מבוסס טכניקה. תוכן בעברית, מבנה באנגלית, Markdown בלבד — כדי שכל
כלי יוכל לקרוא אותו בלי מסד נתונים.

A personal, technique-first recipe archive. Hebrew content, English structure, plain
Markdown. The conventions for working on it live in the repo itself, so any agent that
opens the folder works the same way.

**[INDEX.md](INDEX.md)** — כל המתכונים.

## מה יש כאן

```
recipes/<category>/   המתכונים
guides/               טכניקה שאינה מנה (בניית מחמצת, תסיסה)
logs/                 לוגים — אפיות, מחמצת. append-only
skills/               הקונבנציות, כמיומנות שאפשר להתקין
templates/            תבנית מתכון
scripts/              build_index.py מייצר את INDEX.md
share/                חומר למי שלא עובד עם git
AGENTS.md             מה שכל סוכן קורא ראשון
CLAUDE.md             שורה אחת: @AGENTS.md — בלעדיה Claude Code לא טוען כלום
```

## שימוש עם מודלים

**כל כלי שקורא קבצים** (Codex, Cursor, Gemini CLI, Antigravity): פותחים את התיקייה.
`AGENTS.md` מפנה ל-`skills/recipe-authoring/SKILL.md`, וזה הכל.

**Claude Code** לא קורא `AGENTS.md`. `CLAUDE.md` בשורש מייבא אותו (`@AGENTS.md`) וזה מה
שגורם לזה לעבוד. אל תמחקו אותו. דברים ספציפיים לקלוד — מתחת לשורת הייבוא.

`.agents/skills` הוא סימלינק ל-`skills/`, כי זה הנתיב שסוכנים תואמי-ספק סורקים.

**התקנה כפלאגין ב-Claude Code:**

```
/plugin marketplace add avivlevizky/hamster-food
/plugin install hamster-food@hamster-food
```

שמות הפקודות משתנים בין גרסאות — אם זה לא עובד, בדקו מול התיעוד הרשמי:
https://docs.claude.com/en/docs/claude-code/overview

**בלי git בכלל** (אפליקציית קלוד, נייד): `share/project-instructions-he.md` — טקסט אחד
להדבקה בהוראות פרויקט, שנותן את אותה התנהגות מול תיקייה ב-Google Drive.

## אתר לנייד

`_config.yml` מוכן ל-GitHub Pages. Settings → Pages → Deploy from branch → main / root.
מקבלים URL אחד שנפתח בדפדפן בלי חשבון ובלי אפליקציה — זו הדרך לשתף עם מי שלא רוצה לדעת
מה זה ריפו.

## הוספת מתכון

1. להעתיק את `templates/recipe-template.md` אל `recipes/<category>/<name>.md`
2. למלא frontmatter לפי `skills/recipe-authoring/references/schema.md`
3. `python scripts/build_index.py`

אחרי שינוי בסקיל: `python scripts/validate_skill.py` (או `npx skills-ref validate
skills/recipe-authoring`) — הספציפיקציה סוגרת את רשימת המפתחות ב-frontmatter, וכל מפתח
חורג נופל בוולידציה.

`status` נשאר `untested` עד שבישלתם את זה באמת. זה השדה הכי שימושי כאן בעוד שנה.

## סטטוס

- `guides/sourdough-starter.md` ו-`recipes/bread/panini-di-semola.md` — נכתבו ב-2026-09,
  טרם נאפו.
- `recipes/pasta/pici-rosa-diavola.md` — הועבר מגרסה קודמת (2026-05).
- חסר: פסטה אסאסינה. הטכניקה ידועה, הכמויות צריכות אימות לפני שנכנסות לכאן.
