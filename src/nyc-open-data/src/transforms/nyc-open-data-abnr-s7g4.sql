-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "developerselectiondwid",
    "projectid",
    "_method" AS method,
    "rfpname",
    "rfqname"
FROM "nyc-open-data-abnr-s7g4"
