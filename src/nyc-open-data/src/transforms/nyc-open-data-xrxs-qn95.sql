-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "election_cycle",
    "candidate",
    "board_meeting_date",
    "determination",
    "current_determination_name",
    "final_board_determination"
FROM "nyc-open-data-xrxs-qn95"
