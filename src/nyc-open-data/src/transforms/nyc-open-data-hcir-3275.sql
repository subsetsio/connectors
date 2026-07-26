-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_id",
    "borough",
    "number",
    "street",
    "total_units",
    "aep_start_date",
    "of_bc_violations_at_start",
    "current_status",
    "discharge_date",
    "aep_round",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-hcir-3275"
