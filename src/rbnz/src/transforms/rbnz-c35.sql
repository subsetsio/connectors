-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Workbook rows are published as source observation records; preserve option, file_stem, sheet, indicator_label, series_id, series_name, unit, date, and value when deduplicating or comparing variants.
SELECT
    "series_code",
    "option",
    "file_stem",
    "sheet",
    "indicator_label",
    "series_id",
    "series_name",
    "unit",
    "date",
    "value"
FROM "rbnz-c35"
