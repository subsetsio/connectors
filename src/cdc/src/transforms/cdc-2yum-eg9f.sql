-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Month" AS month,
    "Numerator" AS numerator,
    CAST("Population" AS BIGINT) AS population,
    "Jurisdiction" AS jurisdiction,
    CAST("Estimate" AS DOUBLE) AS estimate,
    "Age_group_label" AS age_group_label,
    "season",
    "legend"
FROM "cdc-2yum-eg9f"
