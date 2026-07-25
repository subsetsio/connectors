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
    CAST("fta_urbanized_area_formula" AS BIGINT) AS fta_urbanized_area_formula,
    CAST("fta_capital_program_5309" AS BIGINT) AS fta_capital_program_5309,
    CAST("fta_rural_progam_5311" AS BIGINT) AS fta_rural_progam_5311,
    CAST("other_fta_funds" AS BIGINT) AS other_fta_funds,
    CAST("other_dot_funds" AS BIGINT) AS other_dot_funds,
    CAST("other_federal_funds" AS BIGINT) AS other_federal_funds,
    CAST("total_federal_funds" AS BIGINT) AS total_federal_funds
FROM "u-s-department-of-transportation-qpjk-b3zw"
