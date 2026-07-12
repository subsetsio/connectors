-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "labour_force_with_other_gainful_activity_not_related_to_holding",
    "indicator",
    "value"
FROM "statistics-estonia-pms246.px"
