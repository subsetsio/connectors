-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "campaign",
    "channel",
    "survey_type",
    "start_time",
    "completion_time",
    "survey_language",
    "overall_satisfaction",
    "wait_time",
    "agent_customer_service",
    "agent_job_knowledge",
    "answer_satisfaction",
    "nps"
FROM "nyc-open-data-kizp-4dfk"
