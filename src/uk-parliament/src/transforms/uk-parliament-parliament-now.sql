-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains current Annunciator messages by chamber; filter `source_endpoint` to separate Commons and Lords records.
SELECT
    "source_entity",
    "source_endpoint",
    "source_skip",
    "record"
FROM "uk-parliament-parliament-now"
