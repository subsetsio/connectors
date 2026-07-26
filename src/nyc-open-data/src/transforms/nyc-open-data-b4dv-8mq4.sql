-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "addr",
    "boro",
    "category",
    "genborough",
    "generating",
    "lat",
    "lon",
    "oer_projec",
    "oer_proj_1",
    "recborough",
    "receiving_" AS receiving,
    "status",
    "uid",
    "volume_cy",
    "weight_ton",
    "location1"
FROM "nyc-open-data-b4dv-8mq4"
