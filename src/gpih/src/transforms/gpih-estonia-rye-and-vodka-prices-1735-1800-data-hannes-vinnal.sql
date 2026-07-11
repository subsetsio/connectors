-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "year",
    "silver ruble" AS silver_ruble,
    "last**" AS last,
    "(g Ag) per liter" AS g_ag_per_liter,
    "aam***" AS aam,
    "per liter" AS per_liter
FROM "gpih-estonia-rye-and-vodka-prices-1735-1800-data-hannes-vinnal"
