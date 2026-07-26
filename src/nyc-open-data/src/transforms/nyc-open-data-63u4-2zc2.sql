-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_code",
    "dbn",
    "school_name",
    "mbps_bandwidth"
FROM "nyc-open-data-63u4-2zc2"
