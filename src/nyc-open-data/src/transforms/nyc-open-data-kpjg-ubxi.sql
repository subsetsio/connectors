-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "initial_contact",
    "language_if_blank_english",
    "issue",
    "date",
    "citystate",
    "zip",
    "cb",
    "council_member",
    "letter_drafted",
    "status"
FROM "nyc-open-data-kpjg-ubxi"
