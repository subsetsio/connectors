-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_id",
    "registration_id",
    "borough",
    "number",
    "street",
    "vacate_order_number",
    "primary_vacate_reason",
    "vacate_type",
    "vacate_effective_date",
    "rescind_date",
    "number_of_vacated_units",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-tb8q-a3ar"
