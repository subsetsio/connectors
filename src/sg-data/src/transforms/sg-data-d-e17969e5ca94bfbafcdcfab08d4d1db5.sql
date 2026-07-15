-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Scholarship_and_Awards" AS scholarship_and_awards,
    "Description" AS description,
    "Reference" AS reference
FROM "sg-data-d-e17969e5ca94bfbafcdcfab08d4d1db5"
