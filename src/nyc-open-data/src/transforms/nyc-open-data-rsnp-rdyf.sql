-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "borrowing_type",
    "borrower",
    "fiscal_year",
    "first_quarter",
    "second_quarter",
    "third_quarter",
    "fourth_quarter"
FROM "nyc-open-data-rsnp-rdyf"
