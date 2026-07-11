-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Local precinct returns mix local offices, jurisdictions, candidates, and reporting modes; filter to a single contest and geography before summing votes.
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
    CAST("writein" AS BOOLEAN) AS writein,
    "state_po",
    "state_fips",
    CAST("state_cen" AS BIGINT) AS state_cen,
    "state_ic",
    CAST("date" AS DATE) AS date,
    CAST("readme_check" AS BOOLEAN) AS readme_check
FROM "mit-election-lab-dvn-chyxup"
