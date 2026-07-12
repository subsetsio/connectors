-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Institution" AS institution,
    "Contract type" AS contract_type,
    "Contract mode" AS contract_mode,
    "Teaching contract" AS teaching_contract,
    "Cost centre" AS cost_centre,
    "Sex" AS sex,
    "Nationality" AS nationality,
    "Notes" AS notes
FROM "statswales-a3b53813-4a38-4caf-83c5-1296e65d075c"
