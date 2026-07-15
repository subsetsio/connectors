-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Others_Total" AS others_total,
    "Others_5_9" AS others_5_9,
    "Others_10_14" AS others_10_14,
    "Others_15_19" AS others_15_19,
    "Others_20_24" AS others_20_24,
    "Others_25_29" AS others_25_29,
    "Others_30_34" AS others_30_34,
    "Others_35_39" AS others_35_39,
    "Others_40_44" AS others_40_44,
    "Others_45_49" AS others_45_49,
    "Others_50_54" AS others_50_54,
    "Others_55_59" AS others_55_59,
    "Others_60_64" AS others_60_64,
    "Others_65_69" AS others_65_69,
    "Others_70_74" AS others_70_74,
    "Others_75_79" AS others_75_79,
    "Others_80_84" AS others_80_84,
    "Others_85andOver" AS others_85andover
FROM "sg-data-d-e751aea72adb041727c4a20dbe31908f"
