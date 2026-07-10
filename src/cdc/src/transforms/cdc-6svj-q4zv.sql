-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("week_ending", '%Y-%m-%d')::DATE AS week_ending,
    CAST("week" AS BIGINT) AS week,
    "season",
    "state",
    "activity_level",
    "activity_level_label"
FROM "cdc-6svj-q4zv"
