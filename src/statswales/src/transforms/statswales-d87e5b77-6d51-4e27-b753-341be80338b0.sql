-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    CAST("Year group" AS BIGINT) AS year_group,
    "FSM eligibility" AS fsm_eligibility,
    "Notes" AS notes
FROM "statswales-d87e5b77-6d51-4e27-b753-341be80338b0"
