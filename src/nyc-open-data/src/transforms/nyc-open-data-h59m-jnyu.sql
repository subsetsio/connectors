-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "category",
    "category_scope",
    "estimate_of_contact",
    "contact_amount"
FROM "nyc-open-data-h59m-jnyu"
