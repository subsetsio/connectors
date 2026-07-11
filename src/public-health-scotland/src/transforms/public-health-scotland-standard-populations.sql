-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    "AgeGroup" AS agegroup,
    CAST("EuropeanStandardPopulation" AS BIGINT) AS europeanstandardpopulation,
    "Sex" AS sex,
    CAST("WorldStandardPopulation" AS BIGINT) AS worldstandardpopulation
FROM "public-health-scotland-standard-populations"
