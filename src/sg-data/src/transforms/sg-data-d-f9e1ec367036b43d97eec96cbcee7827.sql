-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "icd_main_category",
    "icd_detail_category",
    "certified_by",
    "death_count"
FROM "sg-data-d-f9e1ec367036b43d97eec96cbcee7827"
