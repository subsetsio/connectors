-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Chinese_Total" AS chinese_total,
    "Chinese_5_9" AS chinese_5_9,
    "Chinese_10_14" AS chinese_10_14,
    "Chinese_15_19" AS chinese_15_19,
    "Chinese_20_24" AS chinese_20_24,
    "Chinese_25_29" AS chinese_25_29,
    "Chinese_30_34" AS chinese_30_34,
    "Chinese_35_39" AS chinese_35_39,
    "Chinese_40_44" AS chinese_40_44,
    "Chinese_45_49" AS chinese_45_49,
    "Chinese_50_54" AS chinese_50_54,
    "Chinese_55_59" AS chinese_55_59,
    "Chinese_60_64" AS chinese_60_64,
    "Chinese_65_69" AS chinese_65_69,
    "Chinese_70_74" AS chinese_70_74,
    "Chinese_75_79" AS chinese_75_79,
    "Chinese_80_84" AS chinese_80_84,
    "Chinese_85andOver" AS chinese_85andover
FROM "sg-data-d-68860ef451f948e62754a830b6ae5024"
