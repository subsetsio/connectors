-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no._referred" AS no_referred
FROM "sg-data-d-1eace99e11e4d6f593c8b5de89b26e72"
