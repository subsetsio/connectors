-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "School_Name" AS school_name,
    "Subject_Desc" AS subject_desc
FROM "sg-data-d-f1d144e423570c9d84dbc5102c2e664d"
