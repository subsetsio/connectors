-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row represents a successful candidate for a parliamentary constituency; aggregate vote counts only after accounting for constituency-level rows.
SELECT
    CAST("_sl__no_" AS BIGINT) AS sl_no,
    "state",
    CAST("const_no_" AS BIGINT) AS const_no,
    "constituency",
    "constituency_type",
    CAST("total_valid_votes" AS BIGINT) AS total_valid_votes,
    "winner_name",
    "social_category",
    "gender",
    "party",
    "party_symbol",
    CAST("vote_secured" AS BIGINT) AS vote_secured,
    "runner_up_name",
    CAST("margin" AS BIGINT) AS margin,
    CAST("margin__" AS DOUBLE) AS margin_2
FROM "election-commission-of-india-194d454f-3ea8-4621-a915-b211c66e46a7"
