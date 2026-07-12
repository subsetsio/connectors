-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Financial year" AS financial_year,
    "Road class" AS road_class,
    "Work required" AS work_required,
    "Notes" AS notes
FROM "statswales-f91da5a6-166a-4a90-b41e-6e7624a4953c"
