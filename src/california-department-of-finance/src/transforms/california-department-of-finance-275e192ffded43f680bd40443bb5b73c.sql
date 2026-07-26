-- authored pass-through for a 2026-07-26 accept expansion (recollect
-- adopted the DRU 2015-25 wildfire vintage): same faithful-pass-through
-- contract as `hardened compile-transforms` output. Verified pure casts
-- only, no data fixes. Regenerate via model-verify + compile-transforms
-- once this raw is profiled; durable edits belong in the model stage.
SELECT
    CAST("Rank" AS BIGINT) AS rank,
    "County" AS county,
    CAST("Single_Family_Lost" AS BIGINT) AS single_family_lost,
    CAST("Mobile_Home_Lost" AS BIGINT) AS mobile_home_lost,
    CAST("Multi_Family_Lost" AS BIGINT) AS multi_family_lost,
    CAST("Total_Decade_Lost" AS BIGINT) AS total_decade_lost,
    CAST("ObjectId" AS BIGINT) AS objectid
FROM "california-department-of-finance-275e192ffded43f680bd40443bb5b73c"
