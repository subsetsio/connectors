-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains both applications and grants in `metric`; filter the metric before aggregating counts.
-- caution: Includes aggregate origin groupings such as all countries alongside individual countries; filter aggregates before summing across origins.
SELECT
    "country_code",
    "metric",
    CAST("field_id" AS BIGINT) AS field_id,
    CAST("year" AS BIGINT) AS year,
    CAST("value" AS BIGINT) AS value
FROM "epo-patent-applications-grants"
