-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Ranks are event-specific standing snapshots from the export and should not be summed across events or rank scopes.
SELECT
    CAST("best" AS BIGINT) AS best,
    "person_id",
    "event_id",
    CAST("world_rank" AS BIGINT) AS world_rank,
    CAST("continent_rank" AS BIGINT) AS continent_rank,
    CAST("country_rank" AS BIGINT) AS country_rank,
    "_source_table" AS source_table,
    CAST("_export_date" AS TIMESTAMP) AS export_date,
    "_export_version" AS export_version
FROM "wca-ranks-average"
