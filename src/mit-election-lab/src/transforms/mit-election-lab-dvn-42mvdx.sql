-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Presidential rows include multiple candidates and state-level observations across election years; filter to the intended election year and geography before comparing totals.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "state_po",
    CAST("state_fips" AS BIGINT) AS state_fips,
    CAST("state_cen" AS BIGINT) AS state_cen,
    "state_ic",
    "office",
    "candidate",
    "party_detailed",
    "writein",
    CAST("candidatevotes" AS BIGINT) AS candidatevotes,
    CAST("totalvotes" AS BIGINT) AS totalvotes,
    "version",
    "notes",
    "party_simplified"
FROM "mit-election-lab-dvn-42mvdx"
