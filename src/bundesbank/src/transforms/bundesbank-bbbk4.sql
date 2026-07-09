-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long Bundesbank SDMX time-series dataflow: `series_key`/`label` identify source-defined series that can differ by unit, frequency, category, and other attributes; filter those dimensions before aggregating `value`.
-- caution: Use `period_start` for normalized chronological queries and keep `time_period` when the exact upstream period code matters.
SELECT
    "dataflow",
    "file_key",
    "frequency",
    "series_key",
    "label",
    strptime("time_period", '%Y-%m')::DATE AS time_period,
    "period_start",
    "value",
    "flag",
    "unit",
    "unit_en",
    "magnitude",
    "decimals",
    "category",
    "last_update",
    "attributes"
FROM "bundesbank-bbbk4"
