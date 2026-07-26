-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "company_name",
    "company_contact",
    "company_email",
    "company_phone",
    "address",
    "city",
    "state",
    "postcode",
    "industry",
    "industry_descr",
    "company_type",
    "current_fulltime",
    "job_created",
    "job_retain",
    "effective_date",
    "total_savings",
    "savings_from_beginning_receiving_benefits",
    "gas_savings",
    "cogen_savings",
    "electric_savings",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-bug8-9f3g"
