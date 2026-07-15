-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_HDBDwellings_Total" AS total_hdbdwellings_total,
    "Total_HDBDwellings_1_and2_RoomFlats3" AS total_hdbdwellings_1_and2_roomflats3,
    "Total_HDBDwellings_3_RoomFlats" AS total_hdbdwellings_3_roomflats,
    "Total_HDBDwellings_4_RoomFlats" AS total_hdbdwellings_4_roomflats,
    "Total_HDBDwellings_5_RoomandExecutiveFlats" AS total_hdbdwellings_5_roomandexecutiveflats,
    "Total_CondominiumandOtherApartments" AS total_condominiumandotherapartments,
    "Total_LandedProperties" AS total_landedproperties,
    "Total_Others" AS total_others
FROM "sg-data-d-3f87480008efa1a330e571a28ea187e0"
