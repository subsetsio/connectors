-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "capital_source_category",
    "capital_source",
    "years_reported",
    "fiscal_year_1",
    "fiscal_year_1_amount",
    "fiscal_year_2_amount",
    "fiscal_year_3_amount",
    "fiscal_year_4_amount",
    "fiscal_year_5_amount"
FROM "nyc-open-data-4utb-pisg"
