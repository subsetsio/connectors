-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw Statistik Nord table preserved as an independent source publication; consumers should inspect column meanings and aggregation levels before combining across tables.
SELECT
    "entity_id",
    "package_id",
    "package_name",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_url",
    "sheet_name",
    "row_number",
    "column_number",
    "column_label",
    "value_text",
    "value_number",
    "value_date",
    "value_bool"
FROM "statistik-nord-ausfuhr-des-landes-schleswig-holstein-oktober-bis-dezember-2007"
