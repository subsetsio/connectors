-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Authority" AS authority,
    "Planning type" AS planning_type,
    "Notes" AS notes
FROM "statswales-167660cd-ca74-4669-8024-b340e4b8273e"
