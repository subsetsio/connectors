-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "security_type",
    "security_term",
    "reopening",
    "cusip",
    "offering_amt",
    "announcemt_date",
    "auction_date",
    "issue_date"
FROM "us-treasury-fiscal-data-v1-accounting-od-upcoming-auctions"
