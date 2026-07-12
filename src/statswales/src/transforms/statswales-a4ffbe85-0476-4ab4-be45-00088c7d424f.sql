-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year (July to June)" AS year_july_to_june,
    "Tenure" AS tenure,
    "Notes" AS notes
FROM "statswales-a4ffbe85-0476-4ab4-be45-00088c7d424f"
