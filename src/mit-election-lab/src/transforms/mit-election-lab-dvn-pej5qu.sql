-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Senate statewide rows span many election years and candidates; filter by year and state before aggregating votes.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "state_po",
    CAST("state_fips" AS BIGINT) AS state_fips,
    CAST("state_cen" AS DOUBLE) AS state_cen,
    CAST("state_ic" AS BIGINT) AS state_ic,
    "office",
    "district",
    "stage",
    CAST("special" AS BOOLEAN) AS special,
    "candidate",
    "party_detailed",
    CAST("writein" AS BOOLEAN) AS writein,
    "mode",
    CAST("candidatevotes" AS DOUBLE) AS candidatevotes,
    CAST("totalvotes" AS DOUBLE) AS totalvotes,
    CAST("unofficial" AS BOOLEAN) AS unofficial,
    "version",
    "party_simplified"
FROM "mit-election-lab-dvn-pej5qu"
