-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Organisation" AS organisation,
    "Staff group" AS staff_group,
    "Notes" AS notes
FROM "statswales-1998488a-cd5a-4133-843a-4e894df47249"
