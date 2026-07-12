-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Contact" AS contact,
    "Reason for non-contact" AS reason_for_non_contact,
    "Notes" AS notes
FROM "statswales-4224c0ad-ef58-4c6d-9400-704875c3158f"
