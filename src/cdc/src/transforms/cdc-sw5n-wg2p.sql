-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine" AS vaccine,
    "Geographic Level" AS geographic_level,
    "Geographic Name" AS geographic_name,
    "Demographic Level" AS demographic_level,
    "Demographic Name" AS demographic_name,
    "indicator_label",
    "indicator_category_label",
    "Month_Week" AS month_week,
    "Week_ending" AS week_ending,
    CAST("Estimates" AS DOUBLE) AS estimates,
    CAST("CI_Half_width_95pct" AS DOUBLE) AS ci_half_width_95pct,
    CAST("Unweighted Sample Size" AS BIGINT) AS unweighted_sample_size,
    "Influenza_Season" AS influenza_season,
    "suppression_flag"
FROM "cdc-sw5n-wg2p"
