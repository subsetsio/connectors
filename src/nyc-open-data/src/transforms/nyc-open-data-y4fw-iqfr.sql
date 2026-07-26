-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin",
    "system_id",
    "date_registered",
    "number",
    "street",
    "borough",
    "zip_code",
    "sample_dates",
    "active_equip",
    "bbl",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "nta_code"
FROM "nyc-open-data-y4fw-iqfr"
