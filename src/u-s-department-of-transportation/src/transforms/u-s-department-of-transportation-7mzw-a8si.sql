-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("vessel_total_exports_value" AS DOUBLE) AS vessel_total_exports_value,
    CAST("air_total_exports_value_b" AS DOUBLE) AS air_total_exports_value_b,
    CAST("land_total_exports_value" AS DOUBLE) AS land_total_exports_value,
    CAST("vessel_total_imports_value" AS DOUBLE) AS vessel_total_imports_value,
    CAST("air_total_imports_value_b" AS DOUBLE) AS air_total_imports_value_b,
    CAST("land_total_imports_value" AS DOUBLE) AS land_total_imports_value
FROM "u-s-department-of-transportation-7mzw-a8si"
