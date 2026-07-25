-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "tablenumber",
    "type",
    "mode",
    "source",
    "level",
    CAST("year" AS BIGINT) AS year,
    CAST("current_dollar" AS DOUBLE) AS current_dollar,
    CAST("chained_2012_dollars" AS DOUBLE) AS chained_2012_dollars
FROM "u-s-department-of-transportation-nu8j-7gmn"
