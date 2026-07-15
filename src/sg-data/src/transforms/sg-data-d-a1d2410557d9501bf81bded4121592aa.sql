-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "HDBDwellings_Total" AS hdbdwellings_total,
    "HDBDwellings_1_and2_RoomFlats" AS hdbdwellings_1_and2_roomflats,
    "HDBDwellings_3_RoomFlats" AS hdbdwellings_3_roomflats,
    "HDBDwellings_4_RoomFlats" AS hdbdwellings_4_roomflats,
    "HDBDwellings_5_RoomandExecutiveFlats" AS hdbdwellings_5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-a1d2410557d9501bf81bded4121592aa"
