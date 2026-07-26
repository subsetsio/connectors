-- authored pass-through for a 2026-07-26 accept expansion (recollect
-- adopted the DRU 2015-25 wildfire vintage): same faithful-pass-through
-- contract as `hardened compile-transforms` output. Verified pure casts
-- only, no data fixes. Regenerate via model-verify + compile-transforms
-- once this raw is profiled; durable edits belong in the model stage.
SELECT
    CAST("Rank" AS BIGINT) AS rank,
    CAST("Year" AS BIGINT) AS year,
    "Fire_Name_Year" AS fire_name_year,
    "Fire_Fire_and_Year" AS fire_fire_and_year,
    CAST("Single_Family_Lost" AS BIGINT) AS single_family_lost,
    CAST("Mobile_Home_Lost" AS BIGINT) AS mobile_home_lost,
    CAST("Multi_Family_Lost" AS BIGINT) AS multi_family_lost,
    CAST("Total_Housing_Structures_Lost" AS BIGINT) AS total_housing_structures_lost,
    CAST("FID" AS BIGINT) AS fid
FROM "california-department-of-finance-d05e060df7444647aa8e42c2982f951e"
