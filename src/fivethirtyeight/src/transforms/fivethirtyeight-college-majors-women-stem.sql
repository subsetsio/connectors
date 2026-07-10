-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Rank" AS rank,
    "Major_code" AS major_code,
    "Major" AS major,
    "Major_category" AS major_category,
    "Total" AS total,
    "Men" AS men,
    "Women" AS women,
    "ShareWomen" AS sharewomen,
    "Median" AS median
FROM "fivethirtyeight-college-majors-women-stem"
