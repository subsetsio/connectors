-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "certificate_number",
    "business_name",
    "violation_date",
    "industry",
    "borough",
    "charge",
    "charge_number",
    "outcome",
    "counts_settled",
    "counts_guilty",
    "counts_not_guilty",
    "building_number",
    "street",
    "street2",
    "unit_type",
    "unit",
    "description",
    "city",
    "sate",
    "postcode",
    "x_coordinate",
    "y_coordinate",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-wyj6-frpa"
