-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Call category" AS call_category,
    "Local health board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-a3dc253d-2d25-44a0-8410-20a9b9eb5935"
