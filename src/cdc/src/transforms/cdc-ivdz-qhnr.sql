-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Current Season" AS current_season,
    "Month" AS month,
    CAST("Numerator" AS BIGINT) AS numerator,
    CAST("Population" AS BIGINT) AS population,
    "Jurisdiction" AS jurisdiction,
    CAST("Estimate" AS DOUBLE) AS estimate,
    "Age_group_label" AS age_group_label,
    "Legend" AS legend
FROM "cdc-ivdz-qhnr"
