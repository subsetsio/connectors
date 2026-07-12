-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Deprivation group" AS deprivation_group,
    "UK armed forces veterans" AS uk_armed_forces_veterans,
    "Notes" AS notes
FROM "statswales-aa88473f-4e25-4771-b7e4-0243212558ac"
