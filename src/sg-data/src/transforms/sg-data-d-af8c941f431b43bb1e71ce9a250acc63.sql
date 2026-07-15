-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "industry1",
    "industry2",
    "employment_status",
    "employed"
FROM "sg-data-d-af8c941f431b43bb1e71ce9a250acc63"
