-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Sex" AS sex,
    "Collective bargaining" AS collective_bargaining,
    "Notes" AS notes
FROM "statswales-3d51f6dc-f606-45b4-96b4-bee120550c07"
