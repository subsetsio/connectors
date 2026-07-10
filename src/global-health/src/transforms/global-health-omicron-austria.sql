-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This wide weekly table has one row per ISO week and variant counts in separate columns; do not sum across variant columns as if they were independent observations.
SELECT
    "year_week",
    CAST("alpha" AS BIGINT) AS alpha,
    CAST("beta" AS BIGINT) AS beta,
    CAST("gamma" AS BIGINT) AS gamma,
    CAST("delta" AS BIGINT) AS delta,
    CAST("omicron" AS BIGINT) AS omicron,
    CAST("total" AS BIGINT) AS total
FROM "global-health-omicron-austria"
