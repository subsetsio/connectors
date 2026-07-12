-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Rolling 12 month period" AS rolling_12_month_period,
    "Notes" AS notes
FROM "statswales-fa542350-1db8-4508-b60c-e2d254352551"
