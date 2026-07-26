-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "trust_name",
    "expenditure_name",
    "amount",
    "date_of_incurrence",
    "purpose_of_expenditure",
    "attested_by",
    "payee_name",
    "payee_address",
    "city",
    "state",
    "zip_code",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-mhyv-6iza"
