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
    "geocode_source",
    "beat",
    "division",
    "subject_age",
    "subject_race",
    "subject_sex",
    "officer_race",
    "officer_sex",
    "type",
    "violation",
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    CAST("frisk_performed" AS BOOLEAN) AS frisk_performed,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "search_basis",
    "reason_for_search",
    "raw_activity_division",
    "raw_division",
    "raw_activity_beat",
    "raw_beat",
    "raw_driver_race",
    "raw_persons_race",
    "raw_persons_ethnicity",
    "raw_driver_age_range",
    "raw_was_vehcile_searched",
    "raw_citation_location"
FROM "stanford-open-policing-project-ky-louisville"
