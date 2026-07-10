-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "net_approval",
    "Approve" AS approve,
    "Disapprove" AS disapprove,
    "DK/Refused" AS dk_refused
FROM "fivethirtyeight-trump-world-trust-trumpworld-issue-2"
