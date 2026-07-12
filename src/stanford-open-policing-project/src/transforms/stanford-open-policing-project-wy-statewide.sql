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
    "county_name",
    "subject_age",
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    "department_id",
    "type",
    "outcome",
    "raw_race",
    "raw_sex",
    "raw_streetnbr",
    "raw_street"
FROM "stanford-open-policing-project-wy-statewide"
