-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "id",
    CAST("date" AS TIMESTAMP) AS date,
    CAST("year" AS BIGINT) AS year,
    "indicator",
    "measure1",
    "measure2",
    "measure1_description",
    "measure2_description",
    CAST("value1" AS DOUBLE) AS value1,
    "units",
    "note",
    "source"
FROM "u-s-department-of-transportation-y5ut-ibwt"
