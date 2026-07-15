-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "tier",
    "aor",
    "arr",
    "revpar"
FROM "sg-data-d-8da6783d5f7628ae6ada1c240015b7d7"
