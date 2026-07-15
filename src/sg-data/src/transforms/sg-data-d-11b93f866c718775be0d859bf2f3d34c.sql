-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "non_dom_waste_disposed"
FROM "sg-data-d-11b93f866c718775be0d859bf2f3d34c"
