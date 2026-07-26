-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "question_id",
    "question_text",
    "selected_choice",
    "valid_submissions",
    "option_weight",
    "cross_analysis_question_id",
    "cross_analysis_question",
    "cross_analysis_response_weight",
    "cross_analyzed_respondent_count"
FROM "nyc-open-data-irna-apch"
