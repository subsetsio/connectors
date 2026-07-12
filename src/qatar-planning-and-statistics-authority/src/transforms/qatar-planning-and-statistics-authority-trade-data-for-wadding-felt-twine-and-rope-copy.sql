-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "import",
    "export",
    "re_export",
    "export_re_export",
    "net_import",
    "trade_balance"
FROM "qatar-planning-and-statistics-authority-trade-data-for-wadding-felt-twine-and-rope-copy"
