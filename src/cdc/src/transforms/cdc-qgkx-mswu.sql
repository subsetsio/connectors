-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Round" AS BIGINT) AS round,
    "Indicator" AS indicator,
    "Group" AS group,
    "Subgroup" AS subgroup,
    CAST("Sample Size" AS BIGINT) AS sample_size,
    CAST("Percent" AS DOUBLE) AS percent,
    CAST("Standard Error" AS DOUBLE) AS standard_error,
    "Suppression" AS suppression,
    CAST("Significant 1" AS BIGINT) AS significant_1,
    CAST("Significant 2" AS BIGINT) AS significant_2
FROM "cdc-qgkx-mswu"
