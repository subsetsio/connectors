-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Traffic direction and region" AS traffic_direction_and_region,
    "Type of cargo" AS type_of_cargo,
    "Notes" AS notes
FROM "statswales-d3a61e62-8646-4d48-a91b-d009d0e25f7c"
