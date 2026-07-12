-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    strptime("Period", '%d/%m/%Y')::DATE AS period,
    "Tenure" AS tenure,
    "Notes" AS notes
FROM "statswales-6476cc20-ddeb-46a5-be64-10a23c8a159f"
