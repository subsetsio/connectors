-- authored pass-through for a 2026-07-26 accept expansion (recollect
-- adopted the DRU 2015-25 wildfire vintage): same faithful-pass-through
-- contract as `hardened compile-transforms` output. Verified pure casts
-- only, no data fixes. Regenerate via model-verify + compile-transforms
-- once this raw is profiled; durable edits belong in the model stage.
SELECT
    "County" AS county,
    "NAME" AS name,
    "Jurisdiction" AS jurisdiction,
    "Year" AS year,
    CAST("Year123" AS BIGINT) AS year123,
    CAST("Annual_Total_Mobile_Home_Unit" AS BIGINT) AS annual_total_mobile_home_unit,
    CAST("Annual_Total_Multi_Family_Structure" AS BIGINT) AS annual_total_multi_family_structure,
    CAST("Annual_Total_Single_Family_Unit" AS BIGINT) AS annual_total_single_family_unit,
    CAST("Annual_Total_Destroyed_Homes" AS BIGINT) AS annual_total_destroyed_homes,
    CAST("Decade_Total_Mobile_Home_Unit" AS BIGINT) AS decade_total_mobile_home_unit,
    CAST("Decade_Total_Multi_Family_Structure" AS BIGINT) AS decade_total_multi_family_structure,
    CAST("Decade_Total_Single_Family_Unit" AS BIGINT) AS decade_total_single_family_unit,
    CAST("Decade_Total_Destroyed_Homes" AS BIGINT) AS decade_total_destroyed_homes,
    CAST("ObjectId" AS BIGINT) AS objectid,
    "sort" AS sort
FROM "california-department-of-finance-796ce7a8b9bc48e5b4f8c51df6b2d914"
