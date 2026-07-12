-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Provider Health Board" AS provider_health_board,
    "Data Period Quarter" AS data_period_quarter,
    "Conveyance Method" AS conveyance_method,
    "First Place of Safety" AS first_place_of_safety,
    "Notes" AS notes
FROM "statswales-653bd657-5034-44c9-9e8b-31277b2b8a41"
