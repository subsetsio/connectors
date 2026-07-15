-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "Total1" AS total1,
    "HDB1_and2_RoomFlats2" AS hdb1_and2_roomflats2,
    "HDB3_RoomFlats" AS hdb3_roomflats,
    "HDB4_RoomFlats" AS hdb4_roomflats,
    "HDB5_RoomandExecutiveFlats" AS hdb5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-178b6963fe272f50dfd9ceb9411952f9"
