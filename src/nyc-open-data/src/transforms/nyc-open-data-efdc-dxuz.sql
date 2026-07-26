-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_first" AS first,
    "_last" AS last,
    "representative_or_appointee",
    "organization"
FROM "nyc-open-data-efdc-dxuz"
