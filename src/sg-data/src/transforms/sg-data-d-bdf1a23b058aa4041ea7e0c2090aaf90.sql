-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "AgeGroup" AS agegroup,
    "Sex" AS sex,
    "Motivations" AS motivations,
    "Percentage" AS percentage
FROM "sg-data-d-bdf1a23b058aa4041ea7e0c2090aaf90"
