-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "organization_legal_name",
    "address",
    "city",
    "state",
    "postcode",
    "phone",
    "website",
    "project_category_1",
    "project_category_2",
    "total_fiscal_year_funding",
    "funding_source",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-qjvp-rnsx"
