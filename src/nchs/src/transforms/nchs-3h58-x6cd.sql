-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "year",
    "state",
    "county",
    "state_fips_code",
    "county_fips_code",
    "combined_fips_code",
    "birth_rate",
    "lower_confidence_limit",
    "upper_confidence_limit"
FROM "nchs-3h58-x6cd"
