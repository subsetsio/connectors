-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "budget_phase_name",
    "agency_code",
    "agency_name",
    "ua_code",
    "ua_name",
    "borough_name",
    "sub_borough_name",
    "geo_program_name",
    "local_service_district_name",
    "current_modified_budget_amount",
    "current_modified_budget_position",
    "budget_amount",
    "budget_position"
FROM "nyc-open-data-f9xn-fiww"
