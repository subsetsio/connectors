-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a term structure, not a time series: `label` is the forecast horizon in years (1-30), and each remaining column is one model VINTAGE — the expected-inflation curve estimated in that month. It has no time axis of its own.
-- caution: The vintage column NAMES change every month (they encode the vintage month, e.g. `jun_26`), so consumers must not depend on a fixed set of series columns.
SELECT
    CAST("label" AS BIGINT) AS label,
    "jun_26",
    "may_26",
    "jun_25"
FROM "cleveland-fed-inflationexpectations-inflationexpectations-chart3"
