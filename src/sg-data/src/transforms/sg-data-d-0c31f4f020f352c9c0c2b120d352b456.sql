-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "number_of_electronic_searches"
FROM "sg-data-d-0c31f4f020f352c9c0c2b120d352b456"
