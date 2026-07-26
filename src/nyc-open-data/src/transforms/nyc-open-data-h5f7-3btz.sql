-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "agency_name",
    "expense",
    "capital_repair",
    "capital_mitigation"
FROM "nyc-open-data-h5f7-3btz"
