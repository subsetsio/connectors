-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are seasonal waterbody observations; use `froze` and the ice-on/ice-off fields together because some seasons record no freeze-up or thaw date.
SELECT
    "lakecode",
    "lakename",
    "lakeorriver",
    "season",
    CAST("iceon_year" AS BIGINT) AS iceon_year,
    CAST("iceon_month" AS BIGINT) AS iceon_month,
    CAST("iceon_day" AS BIGINT) AS iceon_day,
    CAST("iceoff_year" AS BIGINT) AS iceoff_year,
    CAST("iceoff_month" AS BIGINT) AS iceoff_month,
    CAST("iceoff_day" AS BIGINT) AS iceoff_day,
    CAST("duration" AS BIGINT) AS duration,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "country",
    "froze",
    "comments"
FROM "lake-river-ice-phenology-freeze-thaw"
