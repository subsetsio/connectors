-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are raw oral-question and motion API items with nested JSON in `record`; use source documentation for the fields inside each item.
SELECT
    "source_entity",
    "source_endpoint",
    "source_skip",
    "record"
FROM "uk-parliament-oral-questions-and-motions"
