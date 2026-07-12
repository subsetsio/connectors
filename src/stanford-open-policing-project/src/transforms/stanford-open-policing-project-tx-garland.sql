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
    "time",
    "location",
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    "officer_race",
    "officer_sex",
    "type",
    "disposition",
    "violation",
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    "outcome",
    "speed",
    "posted_speed",
    "vehicle_color",
    "vehicle_make",
    "vehicle_registration_state",
    "vehicle_year",
    "raw_race",
    "raw_alleged_speed",
    "raw_posted_speed"
FROM "stanford-open-policing-project-tx-garland"
