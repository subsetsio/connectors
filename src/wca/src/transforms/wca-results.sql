-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Result values use WCA event-specific encodings for times, means, averages, and penalties; compare values within the same event and format.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("pos" AS BIGINT) AS pos,
    CAST("best" AS BIGINT) AS best,
    CAST("average" AS BIGINT) AS average,
    "competition_id",
    "round_type_id",
    "event_id",
    "person_name",
    "person_id",
    "format_id",
    "regional_single_record",
    "regional_average_record",
    "person_country_id",
    "_source_table" AS source_table,
    CAST("_export_date" AS TIMESTAMP) AS export_date,
    "_export_version" AS export_version
FROM "wca-results"
