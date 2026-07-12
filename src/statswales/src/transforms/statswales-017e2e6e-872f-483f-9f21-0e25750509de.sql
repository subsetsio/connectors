-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Settlement type" AS settlement_type,
    "Domain" AS domain,
    "Deprivation group" AS deprivation_group,
    "Notes" AS notes
FROM "statswales-017e2e6e-872f-483f-9f21-0e25750509de"
