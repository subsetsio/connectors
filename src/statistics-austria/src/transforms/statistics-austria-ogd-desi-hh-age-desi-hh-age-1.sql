-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "federal_states",
    "age",
    "daily_internet_use",
    "at_least_weekly_internet_use",
    "at_least_basic_digital_skills",
    "above_basic_digital_skills",
    "at_least_basic_digital_content_creation_skills",
    "no_internet_use_in_the_last_3_months",
    "e_government_users",
    "e_id_owners",
    "e_id_users",
    "digital_signatures",
    "health_related_information",
    "users_of_generative_ai",
    "users_of_generative_ai_for_private_purposes",
    "users_of_generative_ai_for_professional_purposes",
    "users_of_generative_ai_for_education_or_training_purposes"
FROM "statistics-austria-ogd-desi-hh-age-desi-hh-age-1"
