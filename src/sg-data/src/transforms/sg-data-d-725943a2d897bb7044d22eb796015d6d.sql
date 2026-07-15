-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Malays_Total" AS malays_total,
    "Malays_HDBDwellings_Total" AS malays_hdbdwellings_total,
    "Malays_HDBDwellings_1_and2_RoomFlats3" AS malays_hdbdwellings_1_and2_roomflats3,
    "Malays_HDBDwellings_3_RoomFlats" AS malays_hdbdwellings_3_roomflats,
    "Malays_HDBDwellings_4_RoomFlats" AS malays_hdbdwellings_4_roomflats,
    "Malays_HDBDwellings_5_RoomandExecutiveFlats" AS malays_hdbdwellings_5_roomandexecutiveflats,
    "Malays_CondominiumandOtherApartments" AS malays_condominiumandotherapartments,
    "Malays_LandedProperties" AS malays_landedproperties,
    "Malays_Others" AS malays_others
FROM "sg-data-d-725943a2d897bb7044d22eb796015d6d"
