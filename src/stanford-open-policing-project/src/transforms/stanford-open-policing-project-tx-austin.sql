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
    "date",
    "subject_age",
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    "type",
    "contraband_found",
    "contraband_drugs",
    "contraband_weapons",
    CAST("frisk_performed" AS BOOLEAN) AS frisk_performed,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    CAST("search_person" AS BOOLEAN) AS search_person,
    CAST("search_vehicle" AS BOOLEAN) AS search_vehicle,
    "search_basis",
    "reason_for_stop",
    "vehicle_make",
    "vehicle_model",
    "vehicle_registration_state",
    "vehicle_year",
    "raw_ethnicity",
    "raw_person_search_search_based_on",
    "raw_person_search_search_discovered",
    "raw_person_searched",
    "raw_vehicle_search_search_based_on",
    "raw_vehicle_search_search_discovered",
    "raw_vehicle_searched",
    "raw_race_description",
    "raw_street_check_description"
FROM "stanford-open-policing-project-tx-austin"
