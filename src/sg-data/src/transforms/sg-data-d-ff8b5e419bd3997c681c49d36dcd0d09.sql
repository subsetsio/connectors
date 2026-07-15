-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "HDBDwellings_Total" AS hdbdwellings_total,
    "HDBDwellings_1_And2_RoomFlats" AS hdbdwellings_1_and2_roomflats,
    "HDBDwellings_3_RoomFlats" AS hdbdwellings_3_roomflats,
    "HDBDwellings_4_RoomFlats" AS hdbdwellings_4_roomflats,
    "HDBDwellings_5_RoomAndExecutiveFlats" AS hdbdwellings_5_roomandexecutiveflats,
    "CondominiumsAndOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties,
    "Others" AS others
FROM "sg-data-d-ff8b5e419bd3997c681c49d36dcd0d09"
