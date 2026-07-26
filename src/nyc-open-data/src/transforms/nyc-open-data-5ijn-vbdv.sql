-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unique_key",
    "agency_acronym",
    "agency_name",
    "complaint_type",
    "descriptor",
    "borough",
    "resolution_description",
    "survey_year",
    "survey_month",
    "satisfaction_response",
    "dissatisfaction_reason"
FROM "nyc-open-data-5ijn-vbdv"
