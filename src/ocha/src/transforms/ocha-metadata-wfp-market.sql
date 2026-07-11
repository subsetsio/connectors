-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: WFP market codes are not asserted as globally unique in this connector; use location_code with market code and name when joining or filtering markets.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    CAST("code" AS BIGINT) AS code,
    "name",
    "lat",
    "lon"
FROM "ocha-metadata-wfp-market"
