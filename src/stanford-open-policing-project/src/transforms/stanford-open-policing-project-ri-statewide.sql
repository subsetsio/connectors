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
    "zone",
    "subject_race",
    "subject_sex",
    "department_id",
    "type",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    CAST("contraband_found" AS BOOLEAN) AS contraband_found,
    CAST("contraband_drugs" AS BOOLEAN) AS contraband_drugs,
    CAST("contraband_weapons" AS BOOLEAN) AS contraband_weapons,
    CAST("contraband_alcohol" AS BOOLEAN) AS contraband_alcohol,
    CAST("contraband_other" AS BOOLEAN) AS contraband_other,
    CAST("frisk_performed" AS BOOLEAN) AS frisk_performed,
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    "search_basis",
    "reason_for_search",
    "reason_for_stop",
    "vehicle_make",
    "vehicle_model",
    "raw_BasisForStop" AS raw_basisforstop,
    "raw_OperatorRace" AS raw_operatorrace,
    "raw_OperatorSex" AS raw_operatorsex,
    "raw_ResultOfStop" AS raw_resultofstop,
    "raw_SearchResultOne" AS raw_searchresultone,
    "raw_SearchResultTwo" AS raw_searchresulttwo,
    "raw_SearchResultThree" AS raw_searchresultthree
FROM "stanford-open-policing-project-ri-statewide"
