-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "complaint",
    "date",
    "address",
    "street_name",
    "borough",
    "block",
    "lot",
    "bin",
    "postcode",
    "landmark_name",
    "work_reported",
    "action_taken",
    "status",
    "council_district",
    "community_board",
    "nta",
    "latitude",
    "longitude"
FROM "nyc-open-data-ck4n-5h6x"
