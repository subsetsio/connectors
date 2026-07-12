-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "educational_level",
    "labour_status",
    "group_of_persons",
    "indicator",
    "value"
FROM "statistics-estonia-tt136.px"
