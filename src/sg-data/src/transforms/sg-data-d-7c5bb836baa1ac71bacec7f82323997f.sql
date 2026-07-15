-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "design_class",
    "design_filings",
    "rank"
FROM "sg-data-d-7c5bb836baa1ac71bacec7f82323997f"
