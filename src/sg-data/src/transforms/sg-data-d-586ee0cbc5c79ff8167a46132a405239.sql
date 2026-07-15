-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "schemes_and_subsidies",
    "type"
FROM "sg-data-d-586ee0cbc5c79ff8167a46132a405239"
