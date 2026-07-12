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
    "time",
    "location",
    "beat",
    "subject_age",
    "subject_race",
    "subject_sex",
    CAST("department_id" AS BIGINT) AS department_id,
    "department_name",
    "type",
    "violation",
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    "contraband_found",
    "contraband_drugs",
    "contraband_weapons",
    "search_conducted",
    "search_person",
    "search_vehicle",
    "search_basis",
    "reason_for_stop",
    "vehicle_make",
    "vehicle_year",
    CAST("raw_DriverRace" AS BIGINT) AS raw_driverrace,
    CAST("raw_ReasonForStop" AS BIGINT) AS raw_reasonforstop,
    CAST("raw_TypeOfMovingViolation" AS BIGINT) AS raw_typeofmovingviolation,
    CAST("raw_ResultOfStop" AS BIGINT) AS raw_resultofstop
FROM "stanford-open-policing-project-il-statewide"
