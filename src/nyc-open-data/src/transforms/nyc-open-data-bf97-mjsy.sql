-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin",
    "accident_report_id",
    "incident_date",
    "record_type_description",
    "check2_description",
    "fatality",
    "injury",
    "house_number",
    "street_name",
    "borough",
    "block",
    "lot",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-bf97-mjsy"
