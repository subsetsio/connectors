-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "main_source_of_subsistence",
    "group_of_persons",
    "indicator",
    "value"
FROM "statistics-estonia-tt456.px"
