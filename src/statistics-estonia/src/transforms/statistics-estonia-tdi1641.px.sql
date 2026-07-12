-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "importance",
    "environmental_innovation_factors",
    "number_of_persons_employed",
    "group_of_economic_activities",
    "indicator",
    "value"
FROM "statistics-estonia-tdi1641.px"
