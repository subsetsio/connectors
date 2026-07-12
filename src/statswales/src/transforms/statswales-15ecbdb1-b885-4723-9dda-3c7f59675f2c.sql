-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Specialty" AS specialty,
    "Source of Referral" AS source_of_referral,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-15ecbdb1-b885-4723-9dda-3c7f59675f2c"
