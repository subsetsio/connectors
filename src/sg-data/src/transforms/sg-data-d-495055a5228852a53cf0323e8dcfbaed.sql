-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "service_type",
    "no_of_providers"
FROM "sg-data-d-495055a5228852a53cf0323e8dcfbaed"
