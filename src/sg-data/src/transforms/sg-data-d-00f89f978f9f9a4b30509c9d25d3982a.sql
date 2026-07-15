-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "UpTo15Mins" AS upto15mins,
    "16_30Mins" AS 16_30mins,
    "31_45Mins" AS 31_45mins,
    "46_60Mins" AS 46_60mins,
    "MoreThan60Mins" AS morethan60mins
FROM "sg-data-d-00f89f978f9f9a4b30509c9d25d3982a"
