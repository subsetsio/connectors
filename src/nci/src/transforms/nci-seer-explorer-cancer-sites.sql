-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some site identifiers represent broad cancer sites while others represent subtypes; use the active flag and labels when choosing a reporting universe.
SELECT
    "site_id",
    "site_label",
    "active"
FROM "nci-seer-explorer-cancer-sites"
