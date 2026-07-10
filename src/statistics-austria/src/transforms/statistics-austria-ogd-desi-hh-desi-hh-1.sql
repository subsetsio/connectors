-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "federal_states",
    "daily_internet_usage",
    "at_least_basic_digital_skills",
    "above_basic_digital_skills",
    "at_least_basic_digital_content_creation_skills",
    "no_internet_usage",
    "internet_access",
    "e_government_users",
    "e_id_owners",
    "e_id_users",
    "digital_signatures",
    "health_related_information"
FROM "statistics-austria-ogd-desi-hh-desi-hh-1"
