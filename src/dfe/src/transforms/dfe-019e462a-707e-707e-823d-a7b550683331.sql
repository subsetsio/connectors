-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "fe_sector_type",
    "provider_type",
    "main_role_type",
    "main_subject_taught",
    "staff_count_type",
    CAST("number_staff_responding_providers" AS BIGINT) AS number_staff_responding_providers,
    CAST("number_vacancies_unfilled_responding_providers" AS BIGINT) AS number_vacancies_unfilled_responding_providers,
    CAST("unfilled_vacancy_rate" AS DOUBLE) AS unfilled_vacancy_rate
FROM "dfe-019e462a-707e-707e-823d-a7b550683331"
