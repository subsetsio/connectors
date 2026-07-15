-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "key_uid",
    "key_descriptor",
    "key_vocabulary",
    "relationship_type",
    "related_uid",
    "related_descriptor",
    "related_vocabulary"
FROM "sg-data-d-68955b7991bedbe6d888ad5182974e4f"
