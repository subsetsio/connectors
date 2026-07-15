-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Persons" AS persons,
    "ResidentHouseholds_Total1" AS residenthouseholds_total1,
    "ResidentHouseholds_HDB1_and2_RoomFlats2" AS residenthouseholds_hdb1_and2_roomflats2,
    "ResidentHouseholds_HDB3_RoomFlats" AS residenthouseholds_hdb3_roomflats,
    "ResidentHouseholds_HDB4_RoomFlats" AS residenthouseholds_hdb4_roomflats,
    "ResidentHouseholds_HDB5_RoomandExecutiveFlats" AS residenthouseholds_hdb5_roomandexecutiveflats,
    "ResidentHouseholds_CondominiumsandOtherApartments" AS residenthouseholds_condominiumsandotherapartments,
    "ResidentHouseholds_LandedProperties" AS residenthouseholds_landedproperties,
    "ResidentEmployedHouseholds_Total1" AS residentemployedhouseholds_total1,
    "ResidentEmployedHouseholds_HDB1_and2_RoomFlats2" AS residentemployedhouseholds_hdb1_and2_roomflats2,
    "ResidentEmployedHouseholds_HDB3_RoomFlats" AS residentemployedhouseholds_hdb3_roomflats,
    "ResidentEmployedHouseholds_HDB4_RoomFlats" AS residentemployedhouseholds_hdb4_roomflats,
    "ResidentEmployedHouseholds_HDB5_RoomandExecutiveFlats" AS residentemployedhouseholds_hdb5_roomandexecutiveflats,
    "ResidentEmployedHouseholds_CondominiumsandOtherApartments" AS residentemployedhouseholds_condominiumsandotherapartments,
    "ResidentEmployedHouseholds_LandedProperties" AS residentemployedhouseholds_landedproperties
FROM "sg-data-d-986f584509f939f2fe2d1c48f19bcecc"
