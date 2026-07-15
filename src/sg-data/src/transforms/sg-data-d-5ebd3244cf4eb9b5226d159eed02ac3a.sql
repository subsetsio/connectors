-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "Total3" AS total3,
    "HDBDwellings_TotalHDB4" AS hdbdwellings_totalhdb4,
    "HDBDwellings_1_and2_RoomFlats5" AS hdbdwellings_1_and2_roomflats5,
    "HDBDwellings_3_RoomFlats" AS hdbdwellings_3_roomflats,
    "HDBDwellings_4_RoomFlats" AS hdbdwellings_4_roomflats,
    "HDBDwellings_5_RoomandExecutiveFlats" AS hdbdwellings_5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-5ebd3244cf4eb9b5226d159eed02ac3a"
