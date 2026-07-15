-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Malays_Total" AS malays_total,
    "Malays_5_9" AS malays_5_9,
    "Malays_10_14" AS malays_10_14,
    "Malays_15_19" AS malays_15_19,
    "Malays_20_24" AS malays_20_24,
    "Malays_25_29" AS malays_25_29,
    "Malays_30_34" AS malays_30_34,
    "Malays_35_39" AS malays_35_39,
    "Malays_40_44" AS malays_40_44,
    "Malays_45_49" AS malays_45_49,
    "Malays_50_54" AS malays_50_54,
    "Malays_55_59" AS malays_55_59,
    "Malays_60_64" AS malays_60_64,
    "Malays_65_69" AS malays_65_69,
    "Malays_70_74" AS malays_70_74,
    "Malays_75_79" AS malays_75_79,
    "Malays_80_84" AS malays_80_84,
    "Malays_85andOver" AS malays_85andover
FROM "sg-data-d-9e03755903940847810cd2afd9179970"
