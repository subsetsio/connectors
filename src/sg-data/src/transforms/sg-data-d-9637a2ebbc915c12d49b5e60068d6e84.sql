-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "from",
    "document_type",
    "holding_period",
    "underlying_property_definition",
    "duty_levied_on",
    "duty_formula",
    "duty_rate"
FROM "sg-data-d-9637a2ebbc915c12d49b5e60068d6e84"
