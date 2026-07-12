-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator_id",
    "label",
    "unit",
    "numberformat",
    CAST("group_id" AS BIGINT) AS group_id,
    "datasource",
    "world_all",
    CAST("forecast" AS BIGINT) AS forecast,
    "statistics_from",
    "statistics_to",
    "metadata_json"
FROM "world-steel-indicators"
