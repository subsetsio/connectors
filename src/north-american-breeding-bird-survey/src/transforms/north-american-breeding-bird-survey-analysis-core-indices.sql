-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Modeled annual indices are estimates by species, region, and year; do not aggregate across regions or species without choosing the intended geography and taxon first.
SELECT
    CAST("AOU" AS BIGINT) AS aou,
    "Region" AS region,
    CAST("Year" AS BIGINT) AS year,
    "Index" AS index,
    "2.5%CI" AS "2_5_ci",
    "97.5%CI" AS "97_5_ci"
FROM "north-american-breeding-bird-survey-analysis-core-indices"
