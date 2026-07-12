-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Area" AS area,
    "Section" AS section,
    "Notes" AS notes
FROM "statswales-28f6d701-3833-44ae-80d0-d0c2ffd63ac5"
