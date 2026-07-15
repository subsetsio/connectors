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
    CAST("raw_row_number" AS BIGINT) AS raw_row_number,
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "time",
    "location",
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    "department_id",
    "type",
    "violation",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    CAST("contraband_found" AS BOOLEAN) AS contraband_found,
    CAST("frisk_performed" AS BOOLEAN) AS frisk_performed,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "vehicle_color",
    "vehicle_make",
    "vehicle_model",
    "vehicle_registration_state",
    "raw_TOWNSHIP" AS raw_township,
    "raw_RACE" AS raw_race,
    "raw_Ethnicity" AS raw_ethnicity
FROM "stanford-open-policing-project-nj-statewide"
