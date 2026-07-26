-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are GENESIS-Online observations for one EVAS statistic; `dims` encodes the source cube dimensions and may include totals alongside detailed categories, so filter dimensions before aggregating.
SELECT
    CAST("statistic_code" AS BIGINT) AS statistic_code,
    "table_code",
    "table_name",
    CAST("time" AS BIGINT) AS time,
    "year",
    "measure_code",
    "dims",
    "value",
    "status"
FROM "destatis-22523"
