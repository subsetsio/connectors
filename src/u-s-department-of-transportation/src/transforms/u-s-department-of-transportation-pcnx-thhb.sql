-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("zone_id" AS BIGINT) AS zone_id,
    CAST("lane_number" AS BIGINT) AS lane_number,
    CAST("lane_id" AS BIGINT) AS lane_id,
    CAST("measurement_start" AS TIMESTAMP) AS measurement_start,
    CAST("speed" AS BIGINT) AS speed,
    CAST("volume" AS BIGINT) AS volume,
    CAST("occupancy" AS BIGINT) AS occupancy,
    CAST("quality" AS BIGINT) AS quality
FROM "u-s-department-of-transportation-pcnx-thhb"
