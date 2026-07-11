-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source workbook rows share date and indicator descriptors; workbook context and value identify raw observations.
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
FROM "rbnz-m1"
