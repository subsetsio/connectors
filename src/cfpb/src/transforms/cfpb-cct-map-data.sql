-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a state-level snapshot by market, not a full monthly time series.
SELECT
    CAST("fips_code" AS BIGINT) AS fips_code,
    "state_abbr",
    "value",
    "market"
FROM "cfpb-cct-map-data"
