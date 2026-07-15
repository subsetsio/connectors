-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "Total2" AS total2,
    "HDBDwellings_TotalHDB" AS hdbdwellings_totalhdb,
    "HDBDwellings_1_and2_RoomFlats3" AS hdbdwellings_1_and2_roomflats3,
    "HDBDwellings_3_RoomFlats" AS hdbdwellings_3_roomflats,
    "HDBDwellings_4_RoomFlats" AS hdbdwellings_4_roomflats,
    "HDBDwellings_5_RoomandExecutiveFlats" AS hdbdwellings_5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-4e75c62689c9f6f95ed60c4ad680cb7a"
