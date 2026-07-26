-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "first_name",
    "last_name",
    "appointee_or_representative",
    "term_of_office",
    "term_expiring"
FROM "nyc-open-data-rbwa-m4iy"
