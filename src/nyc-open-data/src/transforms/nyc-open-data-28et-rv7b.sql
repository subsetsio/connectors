-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "identifier",
    "record_title",
    "object_type",
    "date_expression",
    "resource_identifier"
FROM "nyc-open-data-28et-rv7b"
