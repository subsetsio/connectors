-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Quarterly QCEW rows include area, ownership, and NAICS rollups; filter to one rollup level before summing establishments, employment, or wages.
SELECT
    "area_type",
    "area",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    "ownership",
    "naics",
    "naics_title",
    CAST("establishments" AS BIGINT) AS establishments,
    CAST("month_1_employment" AS BIGINT) AS month_1_employment,
    CAST("month_2_employment" AS BIGINT) AS month_2_employment,
    CAST("month_3_employment" AS BIGINT) AS month_3_employment,
    CAST("total_wage" AS BIGINT) AS total_wage
FROM "new-york-state-department-of-labor-cwsm-2ns3"
