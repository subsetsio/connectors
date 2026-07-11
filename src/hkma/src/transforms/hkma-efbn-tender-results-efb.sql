-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Exchange Fund Bills tender rows can repeat by issue date and tenor segment; the source does not publish an issue identifier in this endpoint, so the pass-through table is intentionally keyless.
SELECT
    "issue_date",
    "average_yield_accepted",
    "amount_applied",
    "over_subscription",
    "segment"
FROM "hkma-efbn-tender-results-efb"
