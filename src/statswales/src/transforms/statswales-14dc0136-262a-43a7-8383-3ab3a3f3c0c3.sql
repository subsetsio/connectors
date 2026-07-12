-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Additional Learning Needs (ALN)" AS additional_learning_needs_aln,
    "Subject" AS subject,
    "Notes" AS notes
FROM "statswales-14dc0136-262a-43a7-8383-3ab3a3f3c0c3"
