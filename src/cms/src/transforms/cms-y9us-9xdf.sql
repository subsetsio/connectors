-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Footnote" AS footnote,
    "Footnote Text" AS footnote_text
FROM "cms-y9us-9xdf"
