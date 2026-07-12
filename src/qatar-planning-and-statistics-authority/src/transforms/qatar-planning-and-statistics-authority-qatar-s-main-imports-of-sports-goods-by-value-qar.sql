-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "wsf_lsl",
    "commodity_description",
    "value_qr"
FROM "qatar-planning-and-statistics-authority-qatar-s-main-imports-of-sports-goods-by-value-qar"
