-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This source table has no scan-verified row key in the compact file; multiple observations may exist for a country-year. Treat rows as source observations rather than a unique country-year panel.
-- caution: The meaning and units of value are specific to the Labourers Real Wage indicator and should not be combined with other Clio Infra indicators without consulting the source metadata.
SELECT
    "ccode",
    "country",
    "year",
    "value"
FROM "clio-infra-labourersrealwage"
