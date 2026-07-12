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
    CAST("date" AS VARCHAR) AS date,
    CAST("time" AS VARCHAR) AS time,
    "location",
    "lat",
    "lng",
    "county_name",
    "subject_age",
    "subject_race",
    "subject_sex",
    "department_name",
    "type",
    "violation",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    "frisk_performed",
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "search_basis",
    "reason_for_stop",
    "vehicle_make",
    "vehicle_model",
    "vehicle_type",
    "vehicle_registration_state",
    "vehicle_year",
    "raw_Race" AS raw_race,
    "raw_Ethnicity" AS raw_ethnicity,
    "raw_SearchType" AS raw_searchtype,
    "raw_search_basis"
FROM "stanford-open-policing-project-mt-statewide"
