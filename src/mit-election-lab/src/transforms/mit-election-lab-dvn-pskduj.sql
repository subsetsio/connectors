-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: House precinct returns include detailed candidate and reporting-mode fields; district and mode filters are required for meaningful aggregation.
SELECT
    CAST("year" AS BIGINT) AS year,
    "stage",
    CAST("special" AS BOOLEAN) AS special,
    "state",
    "state_postal",
    CAST("state_fips" AS BIGINT) AS state_fips,
    CAST("state_icpsr" AS BIGINT) AS state_icpsr,
    "county_name",
    "county_fips",
    "county_ansi",
    "county_lat",
    "county_long",
    "jurisdiction",
    "precinct",
    "candidate",
    "candidate_normalized",
    "office",
    "district",
    CAST("writein" AS BOOLEAN) AS writein,
    "party",
    "mode",
    CAST("votes" AS BIGINT) AS votes,
    "candidate_opensecrets",
    "candidate_wikidata",
    "candidate_party",
    "candidate_last",
    "candidate_first",
    "candidate_middle",
    "candidate_full",
    "candidate_suffix",
    "candidate_nickname",
    "candidate_fec",
    "candidate_fec_name",
    "candidate_google",
    "candidate_govtrack",
    "candidate_icpsr",
    "candidate_maplight"
FROM "mit-election-lab-dvn-pskduj"
