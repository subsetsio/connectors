-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are long-form metric observations; pivot or filter `metric` before comparing posts, comments, and score totals.
SELECT
    "metric",
    CAST(to_timestamp("date") AS TIMESTAMP) AS "period_start",
    "value"
FROM "reddit-global-activity"
