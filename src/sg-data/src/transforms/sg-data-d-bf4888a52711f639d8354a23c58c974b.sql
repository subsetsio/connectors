-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Indians_Total" AS indians_total,
    "Indians_5_9" AS indians_5_9,
    "Indians_10_14" AS indians_10_14,
    "Indians_15_19" AS indians_15_19,
    "Indians_20_24" AS indians_20_24,
    "Indians_25_29" AS indians_25_29,
    "Indians_30_34" AS indians_30_34,
    "Indians_35_39" AS indians_35_39,
    "Indians_40_44" AS indians_40_44,
    "Indians_45_49" AS indians_45_49,
    "Indians_50_54" AS indians_50_54,
    "Indians_55_59" AS indians_55_59,
    "Indians_60_64" AS indians_60_64,
    "Indians_65_69" AS indians_65_69,
    "Indians_70_74" AS indians_70_74,
    "Indians_75_79" AS indians_75_79,
    "Indians_80_84" AS indians_80_84,
    "Indians_85andOver" AS indians_85andover
FROM "sg-data-d-bf4888a52711f639d8354a23c58c974b"
