-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Others_Total" AS others_total,
    "Others_HDBDwellings_Total" AS others_hdbdwellings_total,
    "Others_HDBDwellings_1_and2_RoomFlats3" AS others_hdbdwellings_1_and2_roomflats3,
    "Others_HDBDwellings_3_RoomFlats" AS others_hdbdwellings_3_roomflats,
    "Others_HDBDwellings_4_RoomFlats" AS others_hdbdwellings_4_roomflats,
    "Others_HDBDwellings_5_RoomandExecutiveFlats" AS others_hdbdwellings_5_roomandexecutiveflats,
    "Others_CondominiumandOtherApartments" AS others_condominiumandotherapartments,
    "Others_LandedProperties" AS others_landedproperties,
    "Others_Others" AS others_others
FROM "sg-data-d-cb75c3940df4e43a265eb42e69a40b22"
