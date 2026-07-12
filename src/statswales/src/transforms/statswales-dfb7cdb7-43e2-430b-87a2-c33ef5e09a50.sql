-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Before or after housing costs" AS before_or_after_housing_costs,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-dfb7cdb7-43e2-430b-87a2-c33ef5e09a50"
