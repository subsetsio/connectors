-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_year",
    "agency_name",
    "data_set_title",
    "data_set_description",
    "update_frequency",
    "planned_release_date",
    "date_status",
    "agency_comment"
FROM "nyc-open-data-k462-uqyk"
