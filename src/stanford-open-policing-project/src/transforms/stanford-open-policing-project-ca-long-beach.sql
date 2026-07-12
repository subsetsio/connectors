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
    "location",
    "lat",
    "lng",
    "beat",
    "district",
    "subdistrict",
    "division",
    "subject_age",
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    "officer_age",
    "officer_race",
    "officer_sex",
    CAST("officer_years_of_service" AS BIGINT) AS officer_years_of_service,
    "type",
    "violation",
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    "outcome",
    "vehicle_make",
    "vehicle_registration_state",
    "vehicle_year",
    "raw_race",
    "raw_sex",
    "raw_officer_race"
FROM "stanford-open-policing-project-ca-long-beach"
