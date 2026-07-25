-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "agency",
    "city",
    "state",
    "ntd_id",
    "organization_type",
    "reporter_type",
    CAST("report_year" AS BIGINT) AS report_year,
    "uace_code",
    "uza_name",
    CAST("primary_uza_population" AS BIGINT) AS primary_uza_population,
    CAST("agency_voms" AS BIGINT) AS agency_voms,
    CAST("general_fund" AS BIGINT) AS general_fund,
    CAST("income_tax" AS BIGINT) AS income_tax,
    CAST("sales_tax" AS BIGINT) AS sales_tax,
    CAST("property_tax" AS BIGINT) AS property_tax,
    CAST("fuel_tax" AS BIGINT) AS fuel_tax,
    CAST("other_taxes" AS BIGINT) AS other_taxes,
    CAST("tolls" AS BIGINT) AS tolls,
    CAST("other_funds" AS BIGINT) AS other_funds,
    CAST("reduced_reporter_funds" AS BIGINT) AS reduced_reporter_funds,
    CAST("total" AS BIGINT) AS total
FROM "u-s-department-of-transportation-8tvb-ywj3"
