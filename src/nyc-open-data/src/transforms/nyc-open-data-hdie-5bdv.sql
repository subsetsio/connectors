-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "debt_burden_type_1",
    "fiscal_year_1",
    "fiscal_year_1_percent",
    "fiscal_year_2_percent",
    "fiscal_year_3_percent",
    "fiscal_year_4_percent",
    "fiscal_year_5_percent",
    "footnotes"
FROM "nyc-open-data-hdie-5bdv"
