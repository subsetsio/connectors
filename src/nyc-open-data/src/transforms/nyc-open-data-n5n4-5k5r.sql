-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "issuer_name",
    "series_name",
    "new_moneyrefunding",
    "issue_date",
    "tax_exempt_par_amount",
    "taxable_par_amount"
FROM "nyc-open-data-n5n4-5k5r"
