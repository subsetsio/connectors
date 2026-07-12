-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Organisation" AS organisation,
    "Staff group" AS staff_group,
    "Sickness absence reason" AS sickness_absence_reason,
    "Notes" AS notes
FROM "statswales-395828cb-b2e6-495a-9903-3f1f873c110f"
