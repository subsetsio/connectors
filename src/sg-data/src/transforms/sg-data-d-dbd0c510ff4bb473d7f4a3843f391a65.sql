-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "assessable_income",
    "reliefs",
    "chargeable_income",
    "gross_tax",
    "tax_set_offs",
    "net_tax_assessed"
FROM "sg-data-d-dbd0c510ff4bb473d7f4a3843f391a65"
