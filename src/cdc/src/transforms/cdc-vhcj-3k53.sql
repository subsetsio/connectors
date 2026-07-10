-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Season" AS season,
    "Month" AS month,
    "Numerator" AS numerator,
    CAST("Population" AS BIGINT) AS population,
    "Jurisdiction" AS jurisdiction,
    CAST("Estimate" AS DOUBLE) AS estimate,
    "Age_group_label" AS age_group_label
FROM "cdc-vhcj-3k53"
