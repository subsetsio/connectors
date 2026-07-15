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
    "county_name",
    "subject_race",
    "subject_sex",
    "department_id",
    "department_name",
    "type",
    "violation",
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    "outcome",
    "vehicle_make",
    "vehicle_model",
    CAST("vehicle_year" AS BIGINT) AS vehicle_year,
    "raw_ORIG_TRFC_VIOL_CDE" AS raw_orig_trfc_viol_cde,
    "raw_CNTY_NBR" AS raw_cnty_nbr,
    "raw_RACE_IND" AS raw_race_ind,
    "raw_SEX_IND" AS raw_sex_ind
FROM "stanford-open-policing-project-tn-statewide"
