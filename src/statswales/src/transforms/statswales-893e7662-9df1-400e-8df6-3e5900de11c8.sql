-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Actions" AS actions,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-893e7662-9df1-400e-8df6-3e5900de11c8"
