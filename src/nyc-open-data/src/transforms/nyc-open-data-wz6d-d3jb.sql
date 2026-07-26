-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_id",
    "registration_id",
    "borough",
    "house_number",
    "street_name",
    "postcode",
    "of_dwelling_units",
    "infested_dwelling_unit_count",
    "eradicated_unit_count",
    "reinfested_dwelling_unit_count",
    "filing_date",
    "filing_period_start_date",
    "filling_period_end_date",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "_2010_census_tract" AS 2010_census_tract,
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-wz6d-d3jb"
