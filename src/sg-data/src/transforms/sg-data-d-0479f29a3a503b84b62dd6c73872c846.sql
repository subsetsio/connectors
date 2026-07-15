-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "HDBDwellings_Total2" AS hdbdwellings_total2,
    "HDBDwellings_1_And2_RoomFlats3" AS hdbdwellings_1_and2_roomflats3,
    "HDBDwellings_3_RoomFlats" AS hdbdwellings_3_roomflats,
    "HDBDwellings_4_RoomFlats" AS hdbdwellings_4_roomflats,
    "HDBDwellings_5_RoomAndExecutiveFlats" AS hdbdwellings_5_roomandexecutiveflats,
    "CondominiumsAndOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties,
    "Others" AS others
FROM "sg-data-d-0479f29a3a503b84b62dd6c73872c846"
