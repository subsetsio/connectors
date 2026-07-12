-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Welsh port" AS welsh_port,
    "Traffic direction" AS traffic_direction,
    "Notes" AS notes
FROM "statswales-297b0e6f-cd4a-48b1-9fb7-ec2baf02df52"
