-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Farm Size" AS farm_size,
    "Cost Heading" AS cost_heading,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-29942df2-bd99-415f-b870-a3d800e6e778"
