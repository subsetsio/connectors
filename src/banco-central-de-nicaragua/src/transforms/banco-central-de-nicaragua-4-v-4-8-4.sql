-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is a single source-defined measure; use the catalog title and column descriptions for the statistic and unit before comparing values across tables.
SELECT
    "year",
    "col_index",
    "month",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "period_label",
    "value"
FROM "banco-central-de-nicaragua-4-v-4-8-4"
