-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "Total1" AS total1,
    "HDBDwellings_TotalHDB2" AS hdbdwellings_totalhdb2,
    "HDBDwellings_1_and2_RoomFlats3" AS hdbdwellings_1_and2_roomflats3,
    "HDBDwellings_3_RoomFlats" AS hdbdwellings_3_roomflats,
    "HDBDwellings_4_RoomFlats" AS hdbdwellings_4_roomflats,
    "HDBDwellings_5_RoomandExecutiveFlats" AS hdbdwellings_5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-b4b9c25fd6c5e48626bada6e2b517a8b"
