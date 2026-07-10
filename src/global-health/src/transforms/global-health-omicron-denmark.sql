-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This daily table mixes total positive PCR counts with Omicron-specific confirmed and percentage fields; choose the measure column explicitly before aggregating.
SELECT
    "date",
    CAST("total_positive_pcr" AS BIGINT) AS total_positive_pcr,
    CAST("positive_pcr" AS BIGINT) AS positive_pcr,
    CAST("other_variants" AS BIGINT) AS other_variants,
    CAST("inconclusive" AS BIGINT) AS inconclusive,
    CAST("confirmed_omicron" AS BIGINT) AS confirmed_omicron,
    CAST("omicron_percent" AS DOUBLE) AS omicron_percent
FROM "global-health-omicron-denmark"
