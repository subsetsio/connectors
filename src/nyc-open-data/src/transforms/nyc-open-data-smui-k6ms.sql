-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_admin" AS admin,
    "total_complaints",
    "total_violations",
    "disability",
    "ethncity_or_national_origin_or_both",
    "gender",
    "gender_identityexpression",
    "race",
    "religion",
    "sexual_orientation",
    "weight"
FROM "nyc-open-data-smui-k6ms"
