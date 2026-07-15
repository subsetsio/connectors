-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "type_of_relief",
    "no_of_claimants",
    "amount"
FROM "sg-data-d-b08cff1811e8716643614c772f48ba7f"
