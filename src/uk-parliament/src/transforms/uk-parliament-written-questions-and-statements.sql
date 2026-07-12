-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table combines daily-report and written-statement endpoints; filter `source_endpoint` before interpreting the nested `record` schema.
SELECT
    "source_entity",
    "source_endpoint",
    "source_skip",
    "record"
FROM "uk-parliament-written-questions-and-statements"
