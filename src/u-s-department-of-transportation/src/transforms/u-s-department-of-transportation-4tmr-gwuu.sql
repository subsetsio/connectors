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
    "fund_expenditure_type",
    CAST("fares_and_other_directly" AS BIGINT) AS fares_and_other_directly,
    "fares_and_other_directly_1",
    CAST("taxes_fees_levied_by_transit" AS BIGINT) AS taxes_fees_levied_by_transit,
    "taxes_fees_levied_by_transit_1",
    CAST("local" AS BIGINT) AS local,
    "local_questionable",
    CAST("state_1" AS BIGINT) AS state_1,
    "state_questionable",
    CAST("federal" AS BIGINT) AS federal,
    "federal_questionable",
    CAST("total" AS BIGINT) AS total,
    "total_questionable"
FROM "u-s-department-of-transportation-4tmr-gwuu"
