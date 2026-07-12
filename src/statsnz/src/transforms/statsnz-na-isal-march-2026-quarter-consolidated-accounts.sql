-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_reference" AS series_reference,
    CAST("period" AS DOUBLE) AS period,
    CAST("value" AS BIGINT) AS value,
    "Status" AS status,
    "Units" AS units,
    CAST("Magnitude" AS BIGINT) AS magnitude,
    "seasonality",
    "SNA_Account" AS sna_account,
    "Transaction" AS transaction,
    "Transaction_Label" AS transaction_label,
    "Asset_type" AS asset_type,
    "Asset_type_label" AS asset_type_label,
    "Sector" AS sector,
    "Sector_name" AS sector_name,
    "Subject" AS subject,
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month
FROM "statsnz-na-isal-march-2026-quarter-consolidated-accounts"
