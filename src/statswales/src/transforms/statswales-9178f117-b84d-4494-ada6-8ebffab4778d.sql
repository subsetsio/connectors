-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Area" AS area,
    "Successful cases" AS successful_cases,
    "Notes" AS notes
FROM "statswales-9178f117-b84d-4494-ada6-8ebffab4778d"
