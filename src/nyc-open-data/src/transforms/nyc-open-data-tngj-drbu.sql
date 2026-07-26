-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough_name",
    "community_district",
    "total_probationers_ages_16_24",
    "male_probationers_ages_1624",
    "female_probationers_ages_1624"
FROM "nyc-open-data-tngj-drbu"
