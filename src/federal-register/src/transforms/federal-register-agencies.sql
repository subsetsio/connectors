-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "name",
    "short_name",
    "slug",
    "description",
    "parent_id",
    "agency_url",
    "child_count"
FROM "federal-register-agencies"
