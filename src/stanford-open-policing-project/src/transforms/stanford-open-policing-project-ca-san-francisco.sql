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
    "lat",
    "lng",
    "district",
    "subject_age",
    "subject_race",
    "subject_sex",
    "type",
    CAST("arrest_made" AS BOOLEAN) AS arrest_made,
    CAST("citation_issued" AS BOOLEAN) AS citation_issued,
    CAST("warning_issued" AS BOOLEAN) AS warning_issued,
    "outcome",
    "contraband_found",
    CAST("search_conducted" AS BOOLEAN) AS search_conducted,
    CAST("search_vehicle" AS BOOLEAN) AS search_vehicle,
    "search_basis",
    "reason_for_stop",
    "raw_search_vehicle_description",
    "raw_result_of_contact_description"
FROM "stanford-open-policing-project-ca-san-francisco"
