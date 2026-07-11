-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country or economy" AS country_or_economy,
    "Rank" AS rank,
    "Doctorate recipients" AS doctorate_recipients
FROM "ncses-nsf25349-tab007-008"
