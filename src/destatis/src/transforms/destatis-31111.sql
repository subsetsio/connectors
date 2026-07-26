-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are GENESIS-Online observations for EVAS statistic 31111; repeated source observation descriptors are present, so treat rows as keyless and aggregate only after filtering `dims`, `table_code`, and `measure_code` deliberately.
-- caution: The `dims` field encodes source cube dimensions and may include totals alongside detailed categories, so filter dimensions before aggregating.
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
FROM "destatis-31111"
