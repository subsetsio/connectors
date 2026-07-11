-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: House precinct returns are candidate-by-precinct style records; district and reporting-mode filters are required for meaningful aggregation.
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
    CAST("readme_check" AS BOOLEAN) AS readme_check,
    CAST("magnitude" AS BIGINT) AS magnitude
FROM "mit-election-lab-dvn-vlgf2m"
