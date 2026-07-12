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
    "date",
    "location",
    "county_name",
    "subject_age",
    "subject_race",
    "subject_sex",
    "type",
    "arrest_made",
    "citation_issued",
    "warning_issued",
    "outcome",
    "contraband_found",
    "contraband_drugs",
    "contraband_weapons",
    CAST("contraband_alcohol" AS BOOLEAN) AS contraband_alcohol,
    "contraband_other",
    "frisk_performed",
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "search_basis",
    "reason_for_stop",
    "vehicle_type",
    "vehicle_registration_state",
    "raw_Race" AS raw_race
FROM "stanford-open-policing-project-ma-statewide"
