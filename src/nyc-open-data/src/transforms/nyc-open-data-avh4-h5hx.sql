-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "community_advisory_board",
    "_last" AS last,
    "_first" AS first,
    "representative_or_appointee",
    "term_of_office",
    "term_effective",
    "term_expiring",
    "voting"
FROM "nyc-open-data-avh4-h5hx"
