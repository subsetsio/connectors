-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Age" AS age,
    "Accreditation" AS accreditation,
    "Notes" AS notes
FROM "statswales-75f5916c-20ac-4ba3-bc0e-87e3dbaa49d1"
