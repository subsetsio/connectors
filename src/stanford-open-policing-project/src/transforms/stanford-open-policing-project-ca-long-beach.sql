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
    "location",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lng" AS DOUBLE) AS lng,
    CAST("beat" AS BIGINT) AS beat,
    "district",
    CAST("subdistrict" AS BIGINT) AS subdistrict,
    "division",
    CAST("subject_age" AS BIGINT) AS subject_age,
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    CAST("officer_age" AS BIGINT) AS officer_age,
    "officer_race",
    "officer_sex",
    CAST("officer_years_of_service" AS BIGINT) AS officer_years_of_service,
    "type",
    "violation",
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    "outcome",
    "vehicle_make",
    "vehicle_registration_state",
    CAST("vehicle_year" AS BIGINT) AS vehicle_year,
    "raw_race",
    "raw_sex",
    "raw_officer_race"
FROM "stanford-open-policing-project-ca-long-beach"
