-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Constituency election rows mix states, districts, parties, and candidates across many years; filter to the intended election scope before aggregating votes.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "state_po",
    CAST("state_fips" AS BIGINT) AS state_fips,
    CAST("state_cen" AS BIGINT) AS state_cen,
    CAST("state_ic" AS BIGINT) AS state_ic,
    "office",
    "district",
    "stage",
    CAST("special" AS BOOLEAN) AS special,
    "candidate",
    "party_detailed",
    CAST("writein" AS BOOLEAN) AS writein,
    "mode",
    CAST("candidatevotes" AS BIGINT) AS candidatevotes,
    CAST("totalvotes" AS BIGINT) AS totalvotes,
    CAST("unofficial" AS BOOLEAN) AS unofficial,
    CAST("version" AS BIGINT) AS version,
    "party_simplified"
FROM "mit-election-lab-dvn-3cnswo"
