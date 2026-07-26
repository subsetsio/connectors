-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "site",
    "date",
    "giardia_50l",
    "cryptosporidium_50l",
    "qualifiers"
FROM "nyc-open-data-x2s6-6d2j"
