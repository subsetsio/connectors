-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "athlete_id",
    "name",
    "sex",
    strptime("birth_date", '%Y-%m-%d')::DATE AS birth_date,
    "birth_year",
    "height",
    "weight",
    "country",
    "country_noc",
    "description",
    "special_notes"
FROM "base-dos-dados-world-olympedia-olympics--athlete-bio"
