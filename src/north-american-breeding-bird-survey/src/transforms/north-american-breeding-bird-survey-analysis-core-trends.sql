-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Trend estimates are modeled percent-change summaries over the period named in the `Years` column, not annual observations.
SELECT
    "Credibility Code" AS credibility_code,
    "Sample Size Code" AS sample_size_code,
    "Precision Code" AS precision_code,
    "Abundance Code" AS abundance_code,
    "Significance" AS significance,
    CAST("AOU" AS BIGINT) AS aou,
    "Region" AS region,
    "Species" AS species,
    "Region Name" AS region_name,
    "Model" AS model,
    CAST("N Routes" AS BIGINT) AS n_routes,
    CAST("Trend" AS DOUBLE) AS trend,
    CAST("2.5%CI" AS DOUBLE) AS 2_5_ci,
    CAST("97.5%CI" AS DOUBLE) AS 97_5_ci,
    CAST("Relative Abundance" AS DOUBLE) AS relative_abundance,
    "Years" AS years
FROM "north-american-breeding-bird-survey-analysis-core-trends"
