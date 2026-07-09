-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: National coverage only: every row is cober_geo '00' (Estados Unidos Mexicanos). No state or municipal rows are present, so this table cannot be aggregated up from subnational parts.
-- caution: The upstream stream can repeat the same indicator_id/time_period, including exact duplicate rows and rows with different obs_status/value pairs, so this raw table is intentionally keyless.
-- caution: Observations are long-format across indicators of different frequencies and units — never sum or average obs_value across indicator_id without filtering to one indicator, and read unit_id/freq_id before comparing rows.
-- caution: time_period is the source's raw period string and its granularity depends on the series' freq_id (a bare year for annual series, year+period for quarterly/monthly ones); it is not a uniform date.
-- caution: obs_value is expressed in unit_id scaled by unit_mult (a power-of-ten multiplier); the raw number is not directly comparable across series until that scaling is applied.
SELECT
    CAST("indicator_id" AS BIGINT) AS indicator_id,
    "topic_id",
    CAST("freq_id" AS BIGINT) AS freq_id,
    CAST("unit_id" AS BIGINT) AS unit_id,
    "unit_mult",
    "source_id",
    "last_update",
    "time_period",
    CAST("obs_value" AS DOUBLE) AS obs_value,
    CAST("obs_status" AS BIGINT) AS obs_status,
    "obs_exception",
    "obs_note",
    CAST("cober_geo" AS BIGINT) AS cober_geo
FROM "inegi-values"
