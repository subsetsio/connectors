-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "column" AS field_name,
    "description",
    "type",
    "choices",
    "source_resource"
FROM "idb-data-of-violence-against-women-colombia-survey-answers-2014"
