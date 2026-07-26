-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geographic_area_borough",
    "geographic_area_2010_census_fips_county_code",
    "geographic_area_neighborhood_tabulation_area_nta_code",
    "geographic_area_neighborhood_tabulation_area_nta_name",
    "total_population_2000_number",
    "total_population_2010_number",
    "total_population_change_20002010_number",
    "total_population_change_20002010_percent"
FROM "nyc-open-data-rnsn-acs2"
