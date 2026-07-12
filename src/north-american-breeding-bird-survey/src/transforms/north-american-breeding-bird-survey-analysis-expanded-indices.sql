-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Expanded indices use the shorter expanded-coverage analysis window; do not combine them with core indices as if they were the same statistical product.
SELECT
    CAST("AOU" AS BIGINT) AS aou,
    "Region" AS region,
    CAST("Year" AS BIGINT) AS year,
    CAST("Index" AS DOUBLE) AS index,
    CAST("2.5%CI" AS DOUBLE) AS 2_5_ci,
    CAST("97.5%CI" AS DOUBLE) AS 97_5_ci
FROM "north-american-breeding-bird-survey-analysis-expanded-indices"
