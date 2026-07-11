-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fips",
    "year",
    "state",
    "fips_state",
    "county",
    "population",
    "model_based_death_rate",
    "standard_deviation",
    "lower_confidence_limit",
    "upper_confidence_limit",
    "urban_rural_category",
    "census_division"
FROM "nchs-rpvx-m2md"
