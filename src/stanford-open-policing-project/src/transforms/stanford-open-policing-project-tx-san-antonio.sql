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
    "time",
    "location",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lng" AS DOUBLE) AS lng,
    "geocode_source",
    CAST("district" AS BIGINT) AS district,
    "substation",
    CAST("subject_age" AS BIGINT) AS subject_age,
    "subject_race",
    "subject_sex",
    "type",
    "violation",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    "outcome",
    CAST("contraband_found" AS BOOLEAN) AS contraband_found,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "search_basis",
    CAST("speed" AS BIGINT) AS speed,
    CAST("posted_speed" AS BIGINT) AS posted_speed,
    "vehicle_color",
    "vehicle_make",
    "vehicle_model",
    "vehicle_registration_state",
    CAST("vehicle_year" AS BIGINT) AS vehicle_year,
    "raw_race",
    "raw_posted_speed",
    "raw_actual_speed",
    "raw_search_reason",
    "raw_contraband_or_evidence",
    "raw_custodial_arrest_made"
FROM "stanford-open-policing-project-tx-san-antonio"
