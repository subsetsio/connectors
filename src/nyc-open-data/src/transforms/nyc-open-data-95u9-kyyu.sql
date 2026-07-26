-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "neighborhood_advisory_boards",
    "_last" AS last,
    "_first" AS first,
    "appointee_or_representative",
    "appointment_date",
    "term_of_office",
    "term_expiring"
FROM "nyc-open-data-95u9-kyyu"
