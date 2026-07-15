-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "category",
    "sales_of_potable_water"
FROM "sg-data-d-cb1d25dd5cfde21bb9fa704af0e3a962"
