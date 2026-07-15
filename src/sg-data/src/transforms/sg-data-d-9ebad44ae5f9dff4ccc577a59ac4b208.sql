-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Upto15mins" AS upto15mins,
    "16_30mins",
    "31_45mins",
    "46_60mins",
    "Morethan60mins" AS morethan60mins
FROM "sg-data-d-9ebad44ae5f9dff4ccc577a59ac4b208"
