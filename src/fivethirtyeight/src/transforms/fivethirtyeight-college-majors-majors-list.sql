-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FOD1P" AS fod1p,
    "Major" AS major,
    "Major_Category" AS major_category
FROM "fivethirtyeight-college-majors-majors-list"
