-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "indicator_type",
    "21-29" AS 21_29,
    "30-39" AS 30_39,
    "40-49" AS 40_49,
    "50-59" AS 50_59,
    "60-69" AS 60_69,
    "70-79" AS 70_79,
    "80_and_above"
FROM "sg-data-d-bc5b61d5165e43bcf38e22c9e8212b3f"
