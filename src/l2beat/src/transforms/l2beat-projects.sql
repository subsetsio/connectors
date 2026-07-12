-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "name",
    "slug",
    "type",
    "host_chain",
    "category",
    "stage",
    "is_archived",
    "is_under_review",
    "providers",
    "purposes",
    "current_tvs_usd"
FROM "l2beat-projects"
