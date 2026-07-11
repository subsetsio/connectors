-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Population estimates include New York State and county geographies; filter `program_type` and geography level before aggregating.
SELECT
    CAST("fips_code" AS BIGINT) AS fips_code,
    "geography",
    CAST("year" AS BIGINT) AS year,
    "program_type",
    CAST("population" AS BIGINT) AS population
FROM "new-york-state-department-of-labor-krt9-ym2k"
