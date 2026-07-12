-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "reason_for_not_using_generative_ai_tools",
    "group_of_individuals",
    "indicator",
    "value"
FROM "statistics-estonia-it72.px"
