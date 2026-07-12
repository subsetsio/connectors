-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple indicators with different units and both country and regional geographies; join the indicator and geography reference tables or filter those dimensions before comparing or aggregating values.
SELECT
    "indicator_id",
    "geoitem_id",
    CAST("period" AS BIGINT) AS period,
    "year",
    "month",
    "value"
FROM "world-steel-values"
