-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "project",
    "pdf_download",
    "ulurp_application_number"
FROM "nyc-open-data-gt5i-dmde"
