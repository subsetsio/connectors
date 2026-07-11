-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_markets_and_fairs_according_to_organizational_legal_forms_and_period",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-number-20of-20markets-20and-20fairs-by-organizational-legal-forms"
