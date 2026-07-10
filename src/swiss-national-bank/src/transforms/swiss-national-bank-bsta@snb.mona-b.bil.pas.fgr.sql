-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: SNB publishes this as a multidimensional statistical time series; use series_key, series_label, and dimensions_json to select comparable series before aggregating values.
SELECT
    "cube_id",
    "series_key",
    "series_label",
    "dimensions_json",
    "frequency",
    "unit",
    CAST("scale" AS BIGINT) AS scale,
    strptime("period", '%Y-%m')::DATE AS period,
    "period_start",
    "value"
FROM "swiss-national-bank-bsta@snb.mona-b.bil.pas.fgr"
