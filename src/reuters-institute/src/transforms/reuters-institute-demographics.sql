-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "demographic_id",
    "question_label",
    "question_text",
    "option_id",
    "option_label",
    "display_exclusions_json"
FROM "reuters-institute-demographics"
