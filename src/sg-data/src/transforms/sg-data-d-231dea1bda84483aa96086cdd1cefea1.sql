-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "occupation",
    "industry1",
    "industry2",
    "employed"
FROM "sg-data-d-231dea1bda84483aa96086cdd1cefea1"
