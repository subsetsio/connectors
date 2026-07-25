-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("capital_outlay" AS BIGINT) AS capital_outlay,
    CAST("maintenance" AS BIGINT) AS maintenance,
    CAST("admin_law_enforce_bond" AS BIGINT) AS admin_law_enforce_bond,
    CAST("debt_retirement" AS BIGINT) AS debt_retirement
FROM "u-s-department-of-transportation-q989-k45x"
