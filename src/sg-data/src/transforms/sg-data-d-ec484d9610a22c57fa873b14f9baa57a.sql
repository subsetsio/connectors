-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sulphur_dioxide_max_24hour_mean"
FROM "sg-data-d-ec484d9610a22c57fa873b14f9baa57a"
