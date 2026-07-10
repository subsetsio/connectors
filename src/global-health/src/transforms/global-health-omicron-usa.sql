-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are variant-share estimates by week and HHS region or national geography; shares and confidence intervals are not additive counts.
SELECT
    "Day of Week Ending" AS day_of_week_ending,
    "Lineage Bin" AS lineage_bin,
    "Modeltype" AS modeltype,
    "Usa Or Hhsregion" AS usa_or_hhsregion,
    "Variant" AS variant,
    "95CI" AS 95ci,
    CAST("Share" AS DOUBLE) AS share
FROM "global-health-omicron-usa"
