-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organizational_legal_forms",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-transport-20and-20communication-number-20of-20employees-number-of-employees-by-org-legal-forms"
