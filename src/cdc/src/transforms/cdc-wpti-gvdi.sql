-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Outcome (or Indicator)" AS outcome_or_indicator,
    CAST("Percentage" AS DOUBLE) AS percentage,
    "Confidence Interval" AS confidence_interval,
    "Title" AS title,
    "Description" AS description,
    CAST("Year" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    "Year and Quarter" AS year_and_quarter
FROM "cdc-wpti-gvdi"
