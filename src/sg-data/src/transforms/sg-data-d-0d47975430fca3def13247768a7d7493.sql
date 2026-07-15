-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_HDBDwellings_Total" AS total_hdbdwellings_total,
    "Total_HDBDwellings_1_And2_RoomFlats" AS total_hdbdwellings_1_and2_roomflats,
    "Total_HDBDwellings_3_RoomFlats" AS total_hdbdwellings_3_roomflats,
    "Total_HDBDwellings_4_RoomFlats" AS total_hdbdwellings_4_roomflats,
    "Total_HDBDwellings_5_RoomAndExecutiveFlats" AS total_hdbdwellings_5_roomandexecutiveflats,
    "Total_CondominiumsAndOtherApartments" AS total_condominiumsandotherapartments,
    "Total_LandedProperties" AS total_landedproperties,
    "Total_Others" AS total_others,
    "Males_Total" AS males_total,
    "Males_HDBDwellings_Total" AS males_hdbdwellings_total,
    "Males_HDBDwellings_1_And2_RoomFlats" AS males_hdbdwellings_1_and2_roomflats,
    "Males_HDBDwellings_3_RoomFlats" AS males_hdbdwellings_3_roomflats,
    "Males_HDBDwellings_4_RoomFlats" AS males_hdbdwellings_4_roomflats,
    "Males_HDBDwellings_5_RoomAndExecutiveFlats" AS males_hdbdwellings_5_roomandexecutiveflats,
    "Males_CondominiumsAndOtherApartments" AS males_condominiumsandotherapartments,
    "Males_LandedProperties" AS males_landedproperties,
    "Males_Others" AS males_others,
    "Females_Total" AS females_total,
    "Females_HDBDwellings_Total" AS females_hdbdwellings_total,
    "Females_HDBDwellings_1_And2_RoomFlats" AS females_hdbdwellings_1_and2_roomflats,
    "Females_HDBDwellings_3_RoomFlats" AS females_hdbdwellings_3_roomflats,
    "Females_HDBDwellings_4_RoomFlats" AS females_hdbdwellings_4_roomflats,
    "Females_HDBDwellings_5_RoomAndExecutiveFlats" AS females_hdbdwellings_5_roomandexecutiveflats,
    "Females_CondominiumsAndOtherApartments" AS females_condominiumsandotherapartments,
    "Females_LandedProperties" AS females_landedproperties,
    "Females_Others" AS females_others
FROM "sg-data-d-0d47975430fca3def13247768a7d7493"
