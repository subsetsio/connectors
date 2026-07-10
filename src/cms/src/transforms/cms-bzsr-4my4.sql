-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "https://data.cms.gov/provider-data/ location affected" AS https_data_cms_gov_provider_data_location_affected,
    "Downloadable CSV revised file affected" AS downloadable_csv_revised_file_affected,
    "Data Last Updated" AS data_last_updated,
    "Data Last Updated Details" AS data_last_updated_details
FROM "cms-bzsr-4my4"
