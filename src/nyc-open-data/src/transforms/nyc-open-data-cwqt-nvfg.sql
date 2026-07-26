-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "bld_id",
    "school",
    "boro",
    "program_category",
    "reason"
FROM "nyc-open-data-cwqt-nvfg"
