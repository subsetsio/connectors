-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "Upto15mins" AS upto15mins,
    "16_30mins",
    "31_45mins",
    "46_60mins",
    "Morethan60mins" AS morethan60mins
FROM "sg-data-d-50548a3a8084d32a16d68b2ea0e282c0"
