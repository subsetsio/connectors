-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    state,
    CAST(election_date AS DATE) AS election_date,
    election_type,
    election_name,
    reporting_level,
    county,
    precinct,
    office,
    district,
    party,
    candidate,
    CAST(votes AS BIGINT) AS votes
FROM "openelections-mo"
WHERE votes IS NOT NULL
