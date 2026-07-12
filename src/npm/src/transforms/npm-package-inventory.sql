-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The row identity is the registry document revision rather than package name; historical deleted package documents can share package-like names across revisions.
SELECT
    "package",
    "rev"
FROM "npm-package-inventory"
