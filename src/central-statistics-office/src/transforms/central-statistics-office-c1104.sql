-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are source PxStat cells. Tables may include totals or aggregate categories alongside detailed dimension categories, so filter dimension code or label columns before summing values.
SELECT
    "matrix",
    "statistic_code",
    "statistic_label",
    CAST("time_code" AS BIGINT) AS time_code,
    CAST("time_label" AS BIGINT) AS time_label,
    "time_dimension",
    "period_start",
    "period_end",
    "unit",
    "value",
    "dim1_name",
    "dim1_code",
    "dim1_label",
    "dim2_name",
    "dim2_code",
    "dim2_label",
    "dim3_name",
    "dim3_code",
    "dim3_label",
    "dim4_name",
    "dim4_code",
    "dim4_label",
    "dim5_name",
    "dim5_code",
    "dim5_label",
    "dim6_name",
    "dim6_code",
    "dim6_label"
FROM "central-statistics-office-c1104"
