-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Scramble rows identify generated scrambles for competition groups and rounds, not competitor attempts.
SELECT
    "scramble",
    CAST("id" AS BIGINT) AS id,
    "competition_id",
    "event_id",
    "group_id",
    CAST("is_extra" AS BIGINT) AS is_extra,
    "round_type_id",
    CAST("scramble_num" AS BIGINT) AS scramble_num,
    "_source_table" AS source_table,
    CAST("_export_date" AS TIMESTAMP) AS export_date,
    "_export_version" AS export_version
FROM "wca-scrambles"
