-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "race97",
    "label97s",
    "label97l",
    "race77",
    "label77s",
    "label77l",
    "label97min"
FROM "washington-ofm-socrata-9fmr-fbqq"
