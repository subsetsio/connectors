-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual QCEW rows include area, ownership, and NAICS rollups; filter to one rollup level before summing establishments, employment, or wages.
SELECT
    "area_type",
    "area",
    "ownership",
    "naics",
    "naics_title",
    CAST("year" AS BIGINT) AS year,
    CAST("establishments" AS BIGINT) AS establishments,
    CAST("average_employment" AS BIGINT) AS average_employment,
    CAST("total_wage" AS BIGINT) AS total_wage,
    CAST("annual_average_salary" AS BIGINT) AS annual_average_salary
FROM "new-york-state-department-of-labor-shc7-xcbw"
