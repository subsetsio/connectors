-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organizational_legal_forms",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-construction-construction-20by-20kind-20of-20economic-20activity-20nace-20rev-2-value-20added-value-added-by-organizational-legal-forms"
