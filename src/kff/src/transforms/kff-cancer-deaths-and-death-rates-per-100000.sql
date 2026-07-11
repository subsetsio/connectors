-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one cell from a KFF State Health Facts indicator table; do not sum across metrics or locations without first selecting the desired metric/timeframe and excluding aggregate locations when appropriate.
SELECT
    "location",
    CAST("timeframe" AS BIGINT) AS timeframe,
    "col_index",
    "metric",
    CAST("value_raw" AS DOUBLE) AS value_raw,
    "value"
FROM "kff-cancer-deaths-and-death-rates-per-100000"
