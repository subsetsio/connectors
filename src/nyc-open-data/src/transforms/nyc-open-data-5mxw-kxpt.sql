-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_type" AS type,
    "community_education_council",
    "first_name",
    "last_name",
    "appointee_or_representative",
    "term_of_office",
    "term_expiring",
    "voting"
FROM "nyc-open-data-5mxw-kxpt"
