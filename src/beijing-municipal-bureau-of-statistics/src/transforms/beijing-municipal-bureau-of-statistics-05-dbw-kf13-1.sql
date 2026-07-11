-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_number",
    "freq_type",
    "mask",
    "indicator",
    "col_label",
    "value"
FROM "beijing-municipal-bureau-of-statistics-05-dbw-kf13-1"
