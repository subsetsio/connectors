-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number",
    "street",
    "borough",
    "block",
    "lot",
    "bin",
    "saf_type",
    "_primary" AS primary,
    "x",
    "y",
    "geocode_status",
    "construction_status",
    "assignment_type",
    "created_date",
    "last_modified_date",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bbl",
    "nta"
FROM "nyc-open-data-qy7q-cb9e"
