-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_name",
    "alp_domain",
    "alp_title",
    "llp_domain1",
    "llp_title"
FROM "sg-data-d-db1faeea02c646fa3abccfa5aba99214"
