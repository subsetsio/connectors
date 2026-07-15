-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "Total1" AS total1,
    "HDBDwellings_TotalHDB2" AS hdbdwellings_totalhdb2,
    "HDBDwellings_HDB1_and2_RoomFlats3" AS hdbdwellings_hdb1_and2_roomflats3,
    "HDBDwellings_HDB3_RoomFlats" AS hdbdwellings_hdb3_roomflats,
    "HDBDwellings_HDB4_RoomFlats" AS hdbdwellings_hdb4_roomflats,
    "HDBDwellings_HDB5_RoomandExecutiveFlats" AS hdbdwellings_hdb5_roomandexecutiveflats,
    "CondominiumsandOtherApartments" AS condominiumsandotherapartments,
    "LandedProperties" AS landedproperties
FROM "sg-data-d-936bc5a29091b3e41e5a1a962588a653"
