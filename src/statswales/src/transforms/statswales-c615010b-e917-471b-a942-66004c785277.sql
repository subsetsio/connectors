-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Specialty" AS specialty,
    "Organisation" AS organisation,
    "Grade" AS grade,
    "Notes" AS notes
FROM "statswales-c615010b-e917-471b-a942-66004c785277"
