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
    CAST("date" AS VARCHAR) AS date,
    CAST("time" AS VARCHAR) AS time,
    "location",
    "county_name",
    "subject_race",
    "subject_sex",
    "officer_id_hash",
    "type",
    "violation",
    "arrest_made",
    "citation_issued",
    "warning_issued",
    "outcome",
    "contraband_found",
    "contraband_drugs",
    "contraband_other",
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "search_person",
    "search_vehicle",
    "search_basis",
    "reason_for_stop",
    "vehicle_type",
    "vehicle_year",
    "raw_Ethnicity" AS raw_ethnicity,
    "raw_OutcomeOfStop" AS raw_outcomeofstop,
    "raw_ReasonForStop" AS raw_reasonforstop,
    "raw_TypeOfSearch" AS raw_typeofsearch,
    "raw_ViolationsObserved" AS raw_violationsobserved
FROM "stanford-open-policing-project-az-statewide"
