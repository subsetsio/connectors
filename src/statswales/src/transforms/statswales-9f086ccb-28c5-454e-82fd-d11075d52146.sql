-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Type of Disease" AS type_of_disease,
    "Outcome" AS outcome,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-9f086ccb-28c5-454e-82fd-d11075d52146"
