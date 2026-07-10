-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Candidate name" AS candidate_name,
    "Date" AS date,
    "City" AS city,
    "State" AS state,
    "Primary Purpose" AS primary_purpose,
    "Host organization" AS host_organization,
    "Notes" AS notes
FROM "fivethirtyeight-gop-candidate-visits-2024-candidate-visits"
