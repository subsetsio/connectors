-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Senate precinct returns are candidate-by-precinct style records; filter by election, jurisdiction, and reporting mode before aggregation.
SELECT
    "precinct",
    "office",
    "party_detailed",
    "party_simplified",
    "mode",
    "votes",
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
    CAST("state_ic" AS BIGINT) AS state_ic,
    CAST("date" AS DATE) AS date,
    "magnitude"
FROM "mit-election-lab-dvn-zcm3bn"
