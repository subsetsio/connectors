-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: State-by-state precinct files are concatenated into one table; filter by state, contest, geography, and reporting mode before aggregation.
SELECT
    "precinct",
    "office",
    "party_detailed",
    "party_simplified",
    "mode",
    CAST("votes" AS BIGINT) AS votes,
    "county_name",
    "county_fips",
    "jurisdiction_name",
    "jurisdiction_fips",
    "candidate",
    "district",
    CAST("magnitude" AS DOUBLE) AS magnitude,
    "dataverse",
    CAST("year" AS BIGINT) AS year,
    "stage",
    "state",
    CAST("special" AS BOOLEAN) AS special,
    "writein",
    "state_po",
    "state_fips",
    CAST("state_cen" AS BIGINT) AS state_cen,
    "state_ic",
    "date",
    CAST("readme_check" AS BOOLEAN) AS readme_check
FROM "mit-election-lab-dvn-nvqymg"
