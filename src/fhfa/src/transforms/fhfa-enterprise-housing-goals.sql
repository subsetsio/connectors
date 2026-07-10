-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix national and state-level goal performance metrics; filter state before aggregating across geographies.
SELECT
    "state",
    CAST("year" AS BIGINT) AS year,
    "metric",
    CAST("value" AS DOUBLE) AS value
FROM "fhfa-enterprise-housing-goals"
