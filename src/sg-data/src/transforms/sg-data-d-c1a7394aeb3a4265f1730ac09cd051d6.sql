-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "HDB1_and2_RoomFlats1" AS hdb1_and2_roomflats1,
    "HDB3_RoomFlats" AS hdb3_roomflats,
    "HDB4_RoomFlats" AS hdb4_roomflats,
    "HDB5_RoomandExecutiveFlats" AS hdb5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-c1a7394aeb3a4265f1730ac09cd051d6"
