-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "bldg_name",
    "street_name_orig",
    "street_chinese_name",
    "building_chinese_name",
    "attraction"
FROM "sg-data-d-54592963dbd23464b875379a21c2cfe9"
