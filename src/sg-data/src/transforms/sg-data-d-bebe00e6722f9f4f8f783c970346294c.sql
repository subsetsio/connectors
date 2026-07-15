-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Indians_Total" AS indians_total,
    "Indians_HDBDwellings_Total" AS indians_hdbdwellings_total,
    "Indians_HDBDwellings_1_and2_RoomFlats3" AS indians_hdbdwellings_1_and2_roomflats3,
    "Indians_HDBDwellings_3_RoomFlats" AS indians_hdbdwellings_3_roomflats,
    "Indians_HDBDwellings_4_RoomFlats" AS indians_hdbdwellings_4_roomflats,
    "Indians_HDBDwellings_5_RoomandExecutiveFlats" AS indians_hdbdwellings_5_roomandexecutiveflats,
    "Indians_CondominiumandOtherApartments" AS indians_condominiumandotherapartments,
    "Indians_LandedProperties" AS indians_landedproperties,
    "Indians_Others" AS indians_others
FROM "sg-data-d-bebe00e6722f9f4f8f783c970346294c"
