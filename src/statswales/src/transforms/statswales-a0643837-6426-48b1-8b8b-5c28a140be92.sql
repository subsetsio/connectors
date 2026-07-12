-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Organisation" AS organisation,
    "Staff group" AS staff_group,
    "Age band" AS age_band,
    "Disability" AS disability,
    "Ethnic group" AS ethnic_group,
    "Gender" AS gender,
    "Nationality" AS nationality,
    "Notes" AS notes
FROM "statswales-a0643837-6426-48b1-8b8b-5c28a140be92"
