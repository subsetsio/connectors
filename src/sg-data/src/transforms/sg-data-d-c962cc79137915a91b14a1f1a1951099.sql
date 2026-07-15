-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Chinese_Total" AS chinese_total,
    "Chinese_HDBDwellings_Total" AS chinese_hdbdwellings_total,
    "Chinese_HDBDwellings_1_and2_RoomFlats3" AS chinese_hdbdwellings_1_and2_roomflats3,
    "Chinese_HDBDwellings_3_RoomFlats" AS chinese_hdbdwellings_3_roomflats,
    "Chinese_HDBDwellings_4_RoomFlats" AS chinese_hdbdwellings_4_roomflats,
    "Chinese_HDBDwellings_5_RoomandExecutiveFlats" AS chinese_hdbdwellings_5_roomandexecutiveflats,
    "Chinese_CondominiumandOtherApartments" AS chinese_condominiumandotherapartments,
    "Chinese_LandedProperties" AS chinese_landedproperties,
    "Chinese_Others" AS chinese_others
FROM "sg-data-d-c962cc79137915a91b14a1f1a1951099"
