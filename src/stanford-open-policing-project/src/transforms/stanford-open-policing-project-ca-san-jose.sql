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
    CAST("date" AS VARCHAR) AS date,
    CAST("time" AS VARCHAR) AS time,
    "location",
    "lat",
    "lng",
    "subject_race",
    "type",
    "arrest_made",
    "citation_issued",
    "outcome",
    "contraband_found",
    "search_conducted",
    "reason_for_stop",
    "use_of_force_description",
    "use_of_force_reason",
    "raw_search",
    "raw_call_desc",
    "raw_race",
    "raw_event_desc"
FROM "stanford-open-policing-project-ca-san-jose"
