-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix statewide, county, precinct and other reporting levels; filter reporting_level and the relevant jurisdiction columns before aggregating votes.
SELECT
    "state",
    strptime("election_date", '%Y-%m-%d')::DATE AS election_date,
    "election_type",
    "election_name",
    "reporting_level",
    "county",
    "precinct",
    "office",
    CAST("district" AS BIGINT) AS district,
    "party",
    "candidate",
    "votes"
FROM "openelections-wi"
