-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one cell from a KFF State Health Facts indicator table; do not sum across metrics or locations without first selecting the desired metric/timeframe and excluding aggregate locations when appropriate.
SELECT
    "location",
    "timeframe",
    "col_index",
    "metric",
    "value_raw",
    "value"
FROM "kff-number-of-individuals-who-voted-in-thousands-and-individuals-who-voted-as-a-share-of-the-voter-population-by-sex"
