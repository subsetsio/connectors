-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "expectations_for_innovation",
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "number_of_persons_employed",
    "group_of_economic_activities",
    "value"
FROM "statistics-estonia-tdi1613.px"
