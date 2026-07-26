-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_name",
    "asset_number",
    "program_number",
    "subasset",
    "asset_name",
    "street_address",
    "discipline",
    "_system" AS system,
    "component",
    "survey_date",
    "fms_idbudget_code",
    "agency_activity_year",
    "agency_activity_funding"
FROM "nyc-open-data-vck7-ujai"
