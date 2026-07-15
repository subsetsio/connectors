-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "Total4" AS total4,
    "HDBDwellings_TotalHDB" AS hdbdwellings_totalhdb,
    "HDBDwellings_1_and2_RoomFlats5" AS hdbdwellings_1_and2_roomflats5,
    "HDBDwellings_3_RoomFlats" AS hdbdwellings_3_roomflats,
    "HDBDwellings_4_RoomFlats" AS hdbdwellings_4_roomflats,
    "HDBDwellings_5_RoomandExecutiveFlats" AS hdbdwellings_5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-babdc4b2d2dd817021ed66d53555fc4c"
