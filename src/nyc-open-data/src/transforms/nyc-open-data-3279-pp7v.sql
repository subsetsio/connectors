-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "oer_project_numbers",
    "project_name",
    "street_number",
    "street_name",
    "borough",
    "bbl",
    "oer_program",
    "_class" AS class,
    "phase",
    "projectspecific_document_repository_page",
    "latitude",
    "longitude",
    "postcode",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "nta"
FROM "nyc-open-data-3279-pp7v"
