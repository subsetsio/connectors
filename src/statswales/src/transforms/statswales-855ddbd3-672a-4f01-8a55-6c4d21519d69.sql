-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Able to teach in Welsh" AS able_to_teach_in_welsh,
    "Contracted to teach in Welsh" AS contracted_to_teach_in_welsh,
    "Provider" AS provider,
    "Cost centre" AS cost_centre,
    "Contract type" AS contract_type,
    "Contract mode" AS contract_mode,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-855ddbd3-672a-4f01-8a55-6c4d21519d69"
