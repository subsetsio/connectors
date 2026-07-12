-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a refresh/change index for OSV export paths, not the advisory body; use the vulnerability records table for advisory content.
SELECT
    "modified",
    "source_path",
    "source_ecosystem",
    "osv_id"
FROM "osv-modified-ids"
