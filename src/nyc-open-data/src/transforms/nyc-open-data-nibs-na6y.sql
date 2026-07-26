-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "lottery_id",
    "lottery_name",
    "development_type",
    "reporting_construction_type",
    "unit_count",
    "hpd_building_id",
    "housing_connect_building_id",
    "house_number",
    "street_name",
    "borough",
    "unit_distribution_studio",
    "unit_distribution_1_bedroom",
    "unit_distribution_2_bedrooms",
    "unit_distribution_3_bedrooms",
    "unit_distribution_4_bedrooms",
    "applied_income_ami_category_extremely_low_income",
    "applied_income_ami_category_very_low_income",
    "applied_income_ami_category_low_income",
    "applied_income_ami_category_moderate_income",
    "applied_income_ami_category_middle_income",
    "applied_income_ami_category_above_middle_income",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-nibs-na6y"
