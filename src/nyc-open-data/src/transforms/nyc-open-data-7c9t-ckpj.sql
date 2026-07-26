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
    "par_amount",
    "true_interest_cost_tic",
    "longest_maturity",
    "footnote"
FROM "nyc-open-data-7c9t-ckpj"
