-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: County presidential returns are county-level rows; aggregate only within one election year and account for county and state identifiers.
SELECT
    "state",
    "county_name",
    CAST("year" AS BIGINT) AS year,
    "state_po",
    "county_fips",
    "office",
    "candidate",
    "party",
    "candidatevotes",
    CAST("totalvotes" AS BIGINT) AS totalvotes,
    CAST("version" AS BIGINT) AS version,
    "mode"
FROM "mit-election-lab-dvn-voqchq"
