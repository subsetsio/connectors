-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "category",
    "bronx",
    "brooklyn",
    "manhattan",
    "queens",
    "staten_island",
    "citywide"
FROM "nyc-open-data-augs-s4dd"
