-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "kind_of_agricultural_labour_force",
    "county",
    "legal_form_of_holder",
    "indicator",
    "value"
FROM "statistics-estonia-pms241.px"
