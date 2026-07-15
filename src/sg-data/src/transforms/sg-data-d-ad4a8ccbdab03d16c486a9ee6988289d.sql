-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_5_9" AS total_5_9,
    "Total_10_14" AS total_10_14,
    "Total_15_19" AS total_15_19,
    "Total_20_24" AS total_20_24,
    "Total_25_29" AS total_25_29,
    "Total_30_34" AS total_30_34,
    "Total_35_39" AS total_35_39,
    "Total_40_44" AS total_40_44,
    "Total_45_49" AS total_45_49,
    "Total_50_54" AS total_50_54,
    "Total_55_59" AS total_55_59,
    "Total_60_64" AS total_60_64,
    "Total_65_69" AS total_65_69,
    "Total_70_74" AS total_70_74,
    "Total_75_79" AS total_75_79,
    "Total_80_84" AS total_80_84,
    "Total_85andOver" AS total_85andover
FROM "sg-data-d-ad4a8ccbdab03d16c486a9ee6988289d"
