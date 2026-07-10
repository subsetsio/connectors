-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Decade" AS decade,
    "Age" AS age,
    "Male" AS male,
    "Female" AS female,
    "Male_1" AS male_1,
    "Female_1" AS female_1
FROM "fivethirtyeight-most-common-name-aging-curve"
