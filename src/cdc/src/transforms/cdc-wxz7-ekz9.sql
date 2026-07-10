-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Outcome (or Indicator)" AS outcome_or_indicator,
    "Group" AS group,
    CAST("Percentage" AS DOUBLE) AS percentage,
    "Confidence Interval" AS confidence_interval,
    "Title" AS title,
    "Description" AS description,
    CAST("Year" AS BIGINT) AS year
FROM "cdc-wxz7-ekz9"
