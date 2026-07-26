-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "site_id",
    "school_name",
    "_year" AS year,
    "total_enrollment_half_day_full_day",
    "female",
    "female_1",
    "male",
    "male_1",
    "asian",
    "asian_1",
    "black",
    "black_1",
    "hispanic",
    "hispanic_1",
    "other",
    "other_1",
    "white",
    "white_1"
FROM "nyc-open-data-au8p-qz8c"
