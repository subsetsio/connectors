-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "site_id",
    "site_name",
    "site_type",
    "_year" AS year,
    "total_enrollment",
    "asian",
    "asian_1",
    "black",
    "black_1",
    "hispanic",
    "hispanic_1",
    "white",
    "white_1",
    "multiple_race_categories_not_represented",
    "multiple_race_categories_not_represented_1",
    "female",
    "female_1",
    "male",
    "male_1"
FROM "nyc-open-data-u4g8-wkku"
