-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "cargo_type",
    CAST("port_id" AS BIGINT) AS port_id,
    "port_name",
    "region",
    CAST("reporting_year" AS BIGINT) AS reporting_year,
    "state",
    "trade_type",
    "units",
    CAST("port_ranking" AS DOUBLE) AS port_ranking,
    CAST("percent_change" AS DOUBLE) AS percent_change,
    CAST("volume" AS DOUBLE) AS volume
FROM "u-s-department-of-transportation-5rpz-kgm9"
