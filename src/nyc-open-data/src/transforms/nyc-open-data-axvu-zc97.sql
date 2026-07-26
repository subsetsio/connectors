-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acronym",
    "agency",
    "appeal_type",
    "appeal_subtype",
    "date_filed",
    "date_closed",
    "exam_no",
    "expiration",
    "_extension" AS extension,
    "status",
    "title"
FROM "nyc-open-data-axvu-zc97"
