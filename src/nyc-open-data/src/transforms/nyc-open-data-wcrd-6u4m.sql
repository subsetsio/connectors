-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_year",
    "agency_name",
    "mmr_indicator_id",
    "mmr_indicator_name",
    "mmr_indicator_description",
    "mmr_indicator_source",
    "is_the_source_of_this_indicator_on_open_data",
    "nyc_open_data_url",
    "public_statement_from_your_agency_explaining_why_this_data_is_not_being_published"
FROM "nyc-open-data-wcrd-6u4m"
