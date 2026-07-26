-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subway_line_used_most_often",
    "use_of_subway_frequency",
    "get_to_subway_via",
    "primary_use_of_subway",
    "average_length_subway_ride",
    "overall_satisfaction",
    "frequency_of_delays",
    "approximate_delay_duration",
    "alternative_transport",
    "frequency_of_rerouting",
    "top_three_complaints",
    "most_common_reason_for_delay",
    "is_subway_affordable",
    "opinion_on_increased_fares",
    "submitted_at",
    "survey_stop_borough",
    "survey_stop_location",
    "zip_code",
    "collection_method"
FROM "nyc-open-data-4y8i-pbvd"
