-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area of learning" AS area_of_learning,
    "Sex" AS sex,
    "FSM" AS fsm,
    "Notes" AS notes
FROM "statswales-22d3c495-fff4-43d4-964a-1f1452c61cf1"
