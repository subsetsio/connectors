-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Senate county-level results are county observations; filter by election context before summing or comparing vote totals.
SELECT
    CAST("year" AS BIGINT) AS year,
    "date",
    "state",
    "state_po",
    CAST("state_fips" AS BIGINT) AS state_fips,
    CAST("state_cen" AS BIGINT) AS state_cen,
    CAST("state_ic" AS BIGINT) AS state_ic,
    "county_name",
    "county_fips",
    "office",
    "candidate",
    "party_detailed",
    "party_simplified",
    CAST("writein" AS BOOLEAN) AS writein,
    CAST("candidatevotes" AS DOUBLE) AS candidatevotes,
    CAST("totalvotes" AS BIGINT) AS totalvotes,
    CAST("unofficial" AS BOOLEAN) AS unofficial,
    "stage",
    CAST("special" AS BOOLEAN) AS special,
    "mode",
    CAST("version" AS BIGINT) AS version
FROM "mit-election-lab-dvn-yb60ej"
