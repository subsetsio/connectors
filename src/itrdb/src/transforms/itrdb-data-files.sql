-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a file manifest, not parsed tree-ring observations; different file formats require separate domain parsers before measurement values can be analyzed.
-- caution: The same upstream file reference can appear more than once in the Paleo Search nested records, so treat rows as catalog references rather than unique files.
SELECT
    "study_id",
    "site_id",
    "data_table_id",
    "data_table_name",
    "file_url",
    "url_description",
    "link_text",
    "file_extension",
    "time_unit",
    "earliest_year",
    "most_recent_year",
    "earliest_year_bp",
    "most_recent_year_bp",
    "earliest_year_ce",
    "most_recent_year_ce",
    "core_length_meters",
    "data_table_notes",
    "species_json",
    "variables_json",
    "noaa_keywords_json",
    "study_contribution_date"
FROM "itrdb-data-files"
