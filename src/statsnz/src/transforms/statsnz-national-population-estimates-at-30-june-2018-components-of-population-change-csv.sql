-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "period",
    "status",
    CAST("natural_increase" AS BIGINT) AS natural_increase,
    CAST("net_migration" AS BIGINT) AS net_migration,
    CAST("population_change" AS DOUBLE) AS population_change,
    CAST("percent_population_change" AS DOUBLE) AS percent_population_change,
    CAST("population" AS DOUBLE) AS population
FROM "statsnz-national-population-estimates-at-30-june-2018-components-of-population-change-csv"
