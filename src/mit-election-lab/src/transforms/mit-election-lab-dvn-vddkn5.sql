-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Presidential constituency returns span many years and geographies; filter to one election year and constituency level before aggregation.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "state_po",
    CAST("state_fips" AS BIGINT) AS state_fips,
    CAST("state_cen" AS BIGINT) AS state_cen,
    CAST("state_ic" AS BIGINT) AS state_ic,
    "office",
    "candidate",
    "party_detailed",
    "writein",
    CAST("candidatevotes" AS BIGINT) AS candidatevotes,
    CAST("totalvotes" AS BIGINT) AS totalvotes,
    CAST("version" AS BIGINT) AS version,
    "notes",
    "party_simplified"
FROM "mit-election-lab-dvn-vddkn5"
