-- authored pass-through for a 2026-07-26 accept expansion (recollect
-- adopted the DRU 2015-25 wildfire vintage): same faithful-pass-through
-- contract as `hardened compile-transforms` output. Verified pure casts
-- only, no data fixes. Regenerate via model-verify + compile-transforms
-- once this raw is profiled; durable edits belong in the model stage.
SELECT
    CAST("OBJECTID_1" AS BIGINT) AS objectid_1,
    CAST("Shape__Are" AS DOUBLE) AS shape_are,
    CAST("Shape__Len" AS DOUBLE) AS shape_len,
    "County" AS county,
    "CountyFIPS" AS countyfips,
    "FIPS" AS fips,
    "Placecode" AS placecode,
    "JOINNAME" AS joinname,
    "Banner" AS banner,
    CAST("DecadeHU" AS BIGINT) AS decadehu
FROM "california-department-of-finance-95a31702222a4521a6c12cbd11e42fbe"
