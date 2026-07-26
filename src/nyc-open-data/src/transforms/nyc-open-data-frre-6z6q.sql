-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "applicant_name",
    "applicant_house_number",
    "applicant_street_name",
    "applicant_address_2",
    "applicant_city",
    "applicant_state",
    "applicant_postcode",
    "applicant_phone",
    "project_name",
    "project_borough",
    "new_constructionrehabilitation",
    "cra_amount",
    "credit_year",
    "cra_date",
    "total_units",
    "total_tax_credit_units",
    "application_year",
    "applicant_borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020_from_2023",
    "neighborhood_tabulation_area_nta_2020_from_2023"
FROM "nyc-open-data-frre-6z6q"
