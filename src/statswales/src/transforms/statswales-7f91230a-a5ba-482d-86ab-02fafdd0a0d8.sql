-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Ailment" AS ailment,
    "Referral destination" AS referral_destination,
    "Notes" AS notes
FROM "statswales-7f91230a-a5ba-482d-86ab-02fafdd0a0d8"
