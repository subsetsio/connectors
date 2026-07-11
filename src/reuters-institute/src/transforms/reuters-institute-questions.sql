-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "question_id",
    "question_label",
    "question_text",
    "response_type",
    "methodology",
    "option_id",
    "option_label",
    "option_display_exclusions_json",
    "question_display_exclusions_json",
    "demog_exclusions_json",
    "market_basket_label",
    "market_basket_count"
FROM "reuters-institute-questions"
