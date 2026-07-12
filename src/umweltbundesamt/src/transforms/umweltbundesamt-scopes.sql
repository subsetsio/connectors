-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "scope_id",
    "scope_code",
    "scope_time_base",
    "scope_time_scope",
    "scope_time_is_max",
    "scope_name"
FROM "umweltbundesamt-scopes"
