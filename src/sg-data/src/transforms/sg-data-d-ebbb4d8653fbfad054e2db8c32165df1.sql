-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "indicator_type",
    "male",
    "female"
FROM "sg-data-d-ebbb4d8653fbfad054e2db8c32165df1"
