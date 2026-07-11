-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a recent operational snapshot from JMA's bosai surface, not a historical archive; compare observations only within the retained rolling window.
SELECT
    CAST("station_id" AS BIGINT) AS station_id,
    CAST("observed_at" AS TIMESTAMP) AS observed_at,
    "element",
    "value",
    "quality_flag"
FROM "japan-meteorological-agency-amedas-observations"
