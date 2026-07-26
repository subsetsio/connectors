-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_year",
    "agency_name",
    "data_set_title",
    "data_set_description",
    "url_on_agency_website",
    "update_frequency",
    "automatically_updated",
    "already_on_open_data",
    "nyc_open_data_url",
    "scheduled_for_publication",
    "public_statement",
    "status"
FROM "nyc-open-data-duz4-2gn9"
