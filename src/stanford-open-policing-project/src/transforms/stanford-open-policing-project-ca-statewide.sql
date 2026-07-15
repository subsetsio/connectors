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
    "county_name",
    "district",
    "subject_race",
    "subject_sex",
    "department_name",
    "type",
    "violation",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    CAST("contraband_found" AS BOOLEAN) AS contraband_found,
    CAST("frisk_performed" AS BOOLEAN) AS frisk_performed,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    CAST("search_person" AS BOOLEAN) AS search_person,
    "search_basis",
    "reason_for_stop",
    "raw_race",
    "raw_search_basis",
    CAST("raw_location_code" AS BIGINT) AS raw_location_code
FROM "stanford-open-policing-project-ca-statewide"
