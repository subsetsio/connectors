-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Candidate" AS candidate,
    "Incumbent" AS incumbent,
    "State" AS state,
    "Office" AS office,
    "District" AS district,
    "Stance" AS stance,
    "Source" AS source,
    "URL" AS url,
    "Note" AS note
FROM "fivethirtyeight-election-deniers-fivethirtyeight-election-deniers"
