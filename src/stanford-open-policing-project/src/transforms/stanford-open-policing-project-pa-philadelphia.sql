-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Stop-level records for a single published jurisdiction; available fields, raw_* columns, and local coding systems vary by jurisdiction, so compare like columns carefully across tables.
SELECT
    "_source_entity_id" AS source_entity_id,
    "_source_file" AS source_file,
    "_source_member" AS source_member,
    "_row_number" AS row_number,
    "raw_row_number",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "time",
    "location",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lng" AS DOUBLE) AS lng,
    "district",
    "service_area",
    CAST("subject_age" AS BIGINT) AS subject_age,
    "subject_race",
    "subject_sex",
    "type",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    "outcome",
    CAST("contraband_found" AS BOOLEAN) AS contraband_found,
    CAST("frisk_performed" AS BOOLEAN) AS frisk_performed,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    CAST("search_person" AS BOOLEAN) AS search_person,
    CAST("search_vehicle" AS BOOLEAN) AS search_vehicle,
    "raw_race",
    CAST("raw_individual_contraband" AS BOOLEAN) AS raw_individual_contraband,
    CAST("raw_vehicle_contraband" AS BOOLEAN) AS raw_vehicle_contraband
FROM "stanford-open-policing-project-pa-philadelphia"
