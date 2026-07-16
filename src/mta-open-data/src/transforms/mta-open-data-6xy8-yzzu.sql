-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "month_of_year",
    "year",
    "agency",
    "total_incoming_calls",
    "calls_answered",
    "calls_answered_rate",
    "total_wait_time_min",
    "avg_time_to_answer_s",
    "help_point_activations",
    "help_point_total_wait_time",
    "help_point_avg_time_to_answer",
    "social_media_mentions",
    "social_media_responses_sent",
    "social_media_customer",
    "written_feedback_received",
    "written_responses_sent",
    "alerts_and_service_notices",
    "alerts_and_service_notices_1",
    "alerts_and_service_notices_2",
    "alerts_and_service_notices_3",
    "alerts_and_service_notices_4",
    "alerts_and_service_notices_5"
FROM "mta-open-data-6xy8-yzzu"
