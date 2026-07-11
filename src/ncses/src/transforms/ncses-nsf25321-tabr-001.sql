-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "Employed - Never retired - Percent" AS employed_never_retired_percent,
    "Employed - Never retired - SE" AS employed_never_retired_se,
    "Employed - Previously retireda - Percent" AS employed_previously_retireda_percent,
    "Employed - Previously retireda - SE" AS employed_previously_retireda_se,
    "Not employed - Not retiredb - Percent" AS not_employed_not_retiredb_percent,
    "Not employed - Not retiredb - SE" AS not_employed_not_retiredb_se,
    "Not employed - Retiredc - Percent" AS not_employed_retiredc_percent,
    "Not employed - Retiredc - SE" AS not_employed_retiredc_se
FROM "ncses-nsf25321-tabr-001"
