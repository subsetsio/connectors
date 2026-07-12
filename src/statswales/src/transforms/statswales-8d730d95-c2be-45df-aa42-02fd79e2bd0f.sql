-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Country" AS country,
    "Traffic direction" AS traffic_direction,
    "Notes" AS notes
FROM "statswales-8d730d95-c2be-45df-aa42-02fd79e2bd0f"
