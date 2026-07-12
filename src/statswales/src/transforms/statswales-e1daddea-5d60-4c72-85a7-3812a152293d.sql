-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Period end 12 months children 24 months adults", '%d/%m/%Y')::DATE AS period_end_12_months_children_24_months_adults,
    "Area" AS area,
    "Gender" AS gender,
    "Patient Type" AS patient_type,
    "Notes" AS notes
FROM "statswales-e1daddea-5d60-4c72-85a7-3812a152293d"
