-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes monthly, quarterly, and annual observations; filter `frequency` before time-series comparisons or aggregations.
-- caution: The source workbook values do not carry the MEDB catalog `timeseries_id`; the derived `series_key` is not unique across the catalog, so this table is intentionally keyless.
SELECT
    "frequency",
    "series_key",
    "classcode",
    "variable",
    "detail",
    "source",
    "period_label",
    "date",
    "value"
FROM "national-bank-of-slovakia-medb-values"
