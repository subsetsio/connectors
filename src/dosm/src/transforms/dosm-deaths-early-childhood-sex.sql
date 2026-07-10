-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "sex",
    "abs",
    "rate"
FROM "dosm-deaths-early-childhood-sex"
