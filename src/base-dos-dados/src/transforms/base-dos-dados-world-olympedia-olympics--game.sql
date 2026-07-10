-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "edition",
    "edition_id",
    "city",
    "country_flag_url",
    "country_noc",
    strptime("start_date", '%Y-%m-%d')::DATE AS start_date,
    strptime("end_date", '%Y-%m-%d')::DATE AS end_date,
    "competition_date",
    "is_held"
FROM "base-dos-dados-world-olympedia-olympics--game"
