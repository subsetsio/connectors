-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("period_ending" AS TIMESTAMP) AS period_ending,
    "region",
    CAST("initial_claims" AS BIGINT) AS initial_claims
FROM "new-york-state-department-of-labor-w34r-gwfk"
