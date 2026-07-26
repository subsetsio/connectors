-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "lpc",
    "landmark_name",
    "street",
    "street_name",
    "boro",
    "block",
    "lot",
    "vio_date",
    "wl_date",
    "nov_date",
    "violation_text",
    "status",
    "rescended_date",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "nta",
    "postcode"
FROM "nyc-open-data-wycc-5aqt"
