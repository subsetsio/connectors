-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple aggregation dimensions in one long table; filter aggregation before comparing or summing categories.
-- caution: Contains both monthly and weekly observations; filter timestep before time-series analysis.
SELECT
    "timestep",
    "aggregation",
    "category",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "ner",
    "ner_sa"
FROM "adp-ner-employment"
