-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FN_ID" AS fn_id,
    "FN_TEXT" AS fn_text
FROM "cdc-gjsp-ircr"
