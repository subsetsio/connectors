-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("_sl__no_" AS BIGINT) AS sl_no,
    "party_type",
    CAST("no_of_parties_participated" AS BIGINT) AS no_of_parties_participated
FROM "election-commission-of-india-82be928f-4679-47f5-9512-2d06cf503212"
