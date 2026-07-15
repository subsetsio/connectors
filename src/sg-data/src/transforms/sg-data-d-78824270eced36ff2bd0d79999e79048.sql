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
FROM "sg-data-d-78824270eced36ff2bd0d79999e79048"
