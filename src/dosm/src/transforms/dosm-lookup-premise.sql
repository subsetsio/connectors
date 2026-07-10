-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "premise_code",
    "premise",
    "address",
    "premise_type",
    "state",
    "district"
FROM "dosm-lookup-premise"
