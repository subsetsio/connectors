-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "series",
    "period",
    "year",
    "part",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "value"
FROM "monetary-authority-of-macao-8-fsiwebinfotimeseries--fsi-time-series-2010q1-present"
