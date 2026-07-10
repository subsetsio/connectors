-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_starting_1995" AS BIGINT) AS year_starting_1995,
    "goods_sitc",
    "partnergrou_s_countries",
    "imports_in_1_000_eur",
    "exports_in_1_000_eur",
    "balance_of_foreign_trade_in_1_000_eur"
FROM "statistics-austria-ogd-watlas12-watlas-12"
