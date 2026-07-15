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
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lng" AS DOUBLE) AS lng,
    "county_name",
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    "department_name",
    "type",
    "violation",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    CAST("contraband_found" AS BOOLEAN) AS contraband_found,
    CAST("contraband_drugs" AS BOOLEAN) AS contraband_drugs,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "search_basis",
    "raw_DISP_STRING" AS raw_disp_string,
    "raw_ORC_STRING" AS raw_orc_string,
    "raw_DISPOSITIONS" AS raw_dispositions,
    "raw_race"
FROM "stanford-open-policing-project-oh-statewide"
