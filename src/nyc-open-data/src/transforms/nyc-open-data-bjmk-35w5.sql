-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "program_name",
    "district",
    "building_id",
    "school_name",
    "borough",
    "constrstart_fy",
    "description"
FROM "nyc-open-data-bjmk-35w5"
