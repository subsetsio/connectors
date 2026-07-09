-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each bilateral relationship is stored as two mirrored rows, (country, partner) and (partner, country): a flow appears once as the reporter's `export_value` and again as the partner row's `import_value`. Sum `export_value` alone (or `import_value` alone) for world totals — adding both across all rows double-counts every flow.
SELECT
    "country_id",
    "country_iso3_code",
    "partner_country_id",
    "partner_iso3_code",
    "year",
    "export_value",
    "import_value"
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs92-country-country-year"
