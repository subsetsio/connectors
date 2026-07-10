-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "d",
    "data_anchor_x",
    "data_anchor_y",
    "data_fill_id",
    "data_name",
    "id",
    "filename"
FROM "drees-formes-geographiques-des-regions-en-svg"
