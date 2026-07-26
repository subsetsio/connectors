-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "press_release_date",
    "press_release_title",
    "link_to_pdf_file"
FROM "nyc-open-data-kewa-q4dq"
