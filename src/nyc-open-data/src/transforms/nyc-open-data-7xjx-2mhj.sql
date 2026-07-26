-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "bldg_id",
    "school",
    "boro",
    "program_category"
FROM "nyc-open-data-7xjx-2mhj"
