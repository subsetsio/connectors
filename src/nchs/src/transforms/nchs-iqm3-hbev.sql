-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dataset_shortname",
    "footnote_id_list",
    "fn_type",
    "fn_code",
    "fn_text"
FROM "nchs-iqm3-hbev"
