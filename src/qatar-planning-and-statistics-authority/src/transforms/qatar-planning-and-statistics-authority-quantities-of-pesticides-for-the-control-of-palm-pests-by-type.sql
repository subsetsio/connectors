-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type",
    "lnw",
    "unit",
    "lwhd",
    "quantity"
FROM "qatar-planning-and-statistics-authority-quantities-of-pesticides-for-the-control-of-palm-pests-by-type"
