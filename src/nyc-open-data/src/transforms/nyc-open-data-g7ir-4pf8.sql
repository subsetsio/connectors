-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_of_speech",
    "speaker",
    "law_speech_title",
    "link_to_pdf_file"
FROM "nyc-open-data-g7ir-4pf8"
