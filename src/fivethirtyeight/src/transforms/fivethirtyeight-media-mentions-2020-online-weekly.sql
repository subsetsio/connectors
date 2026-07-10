-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "name",
    "matched_stories",
    "all_candidate_stories",
    "pct_of_all_candidate_stories",
    "query"
FROM "fivethirtyeight-media-mentions-2020-online-weekly"
