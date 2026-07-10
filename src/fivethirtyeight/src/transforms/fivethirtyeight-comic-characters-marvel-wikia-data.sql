-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "page_id",
    "name",
    "urlslug",
    "ID" AS id,
    "ALIGN" AS align,
    "EYE" AS eye,
    "HAIR" AS hair,
    "SEX" AS sex,
    "GSM" AS gsm,
    "ALIVE" AS alive,
    "APPEARANCES" AS appearances,
    "FIRST APPEARANCE" AS first_appearance,
    "Year" AS year
FROM "fivethirtyeight-comic-characters-marvel-wikia-data"
