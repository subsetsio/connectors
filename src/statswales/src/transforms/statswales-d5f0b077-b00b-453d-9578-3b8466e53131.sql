-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Period end 12 months children 24 months adults", '%d/%m/%Y')::DATE AS period_end_12_months_children_24_months_adults,
    "Area" AS area,
    "Ethnicity" AS ethnicity,
    "Patient Type" AS patient_type,
    "Notes" AS notes
FROM "statswales-d5f0b077-b00b-453d-9578-3b8466e53131"
