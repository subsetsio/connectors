-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Gender" AS gender,
    "Age at adoption" AS age_at_adoption,
    "Notes" AS notes
FROM "statswales-a0b8bb13-ea6e-413c-8a0c-0e11ef2cbfe2"
