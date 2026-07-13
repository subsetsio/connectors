-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    CAST("expected_solve_count" AS BIGINT) AS expected_solve_count,
    "name",
    "sort_by",
    "sort_by_second",
    CAST("trim_fastest_n" AS BIGINT) AS trim_fastest_n,
    CAST("trim_slowest_n" AS BIGINT) AS trim_slowest_n,
    "_source_table" AS source_table,
    CAST("_export_date" AS TIMESTAMP) AS export_date,
    "_export_version" AS export_version
FROM "wca-formats"
