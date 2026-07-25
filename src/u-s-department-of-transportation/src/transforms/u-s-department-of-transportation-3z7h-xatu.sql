-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("unnamed_column" AS BIGINT) AS unnamed_column,
    "row_labels",
    CAST("sum_of_total_pax" AS BIGINT) AS sum_of_total_pax
FROM "u-s-department-of-transportation-3z7h-xatu"
