-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_reference" AS series_reference,
    CAST("Period" AS DOUBLE) AS period,
    CAST("Value" AS BIGINT) AS value,
    "Unit" AS unit,
    "Seasonality" AS seasonality,
    "Series_name" AS series_name,
    "RBNZ_seriesID" AS rbnz_seriesid,
    "Transaction" AS transaction,
    "Transaction_label" AS transaction_label,
    "Asset_type" AS asset_type,
    CAST("Sector" AS BIGINT) AS sector,
    "Sector_name" AS sector_name
FROM "statsnz-na-isal-march-2026-quarter-supplementary-table-1-5b"
