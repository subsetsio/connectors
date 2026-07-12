-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The normalized table has repeated year and metric labels for distinct source concepts, with the distinguishing context embedded only in the source labels; do not aggregate by `category` and `metric` without reviewing the metric labels.
SELECT
    "region",
    CAST("category" AS BIGINT) AS category,
    "metric",
    "value"
FROM "damodaran-histretsp"
