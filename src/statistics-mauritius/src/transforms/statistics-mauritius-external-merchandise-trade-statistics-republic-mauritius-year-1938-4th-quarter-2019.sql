-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The package combines annual and quarterly merchandise trade resources, so time periods are not all the same granularity.
SELECT
    "Period" AS period,
    CAST("Exports_of_goods_(F.O.B)" AS BIGINT) AS exports_of_goods_f_o_b,
    "Domestic_exports" AS domestic_exports,
    "Re-exports" AS re_exports,
    "Ships_Stores_and_Bunkers" AS ships_stores_and_bunkers,
    CAST("Total_Exports_(F.O.B)" AS BIGINT) AS total_exports_f_o_b,
    CAST("Export_Oriented_Enterprises_out_of_Total_Exports" AS BIGINT) AS export_oriented_enterprises_out_of_total_exports,
    CAST("Total_Imports_(C.I.F)" AS BIGINT) AS total_imports_c_i_f,
    CAST("Export_Oriented_Enterprises_out_of_Total_Imports" AS BIGINT) AS export_oriented_enterprises_out_of_total_imports,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified,
    CAST("Year" AS BIGINT) AS year
FROM "statistics-mauritius-external-merchandise-trade-statistics-republic-mauritius-year-1938-4th-quarter-2019"
