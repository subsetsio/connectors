-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Performer" AS performer,
    "Show" AS show,
    "Show Start" AS show_start,
    "Show End" AS show_end,
    "Status?" AS status,
    "CharEnd" AS charend,
    "Years Since" AS years_since,
    "#LEAD" AS lead,
    "#SUPPORT" AS support,
    "#Shows" AS shows,
    "Score" AS score,
    "Score/Y" AS score_y,
    "lead_notes",
    "support_notes",
    "show_notes"
FROM "fivethirtyeight-mad-men-show-data"
