-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "coast",
    CAST("sum_of_containerized_vessel" AS BIGINT) AS sum_of_containerized_vessel
FROM "u-s-department-of-transportation-mjx8-bw4c"
