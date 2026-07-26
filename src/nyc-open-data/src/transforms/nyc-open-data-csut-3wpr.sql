-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "prevelance",
    "_year" AS year,
    "no_health_insurance",
    "did_not_get_needed_medical_care",
    "no_personal_doctor",
    "drinks_1_or_more_sugarsweetened_beverages_per_day",
    "smoking_status_current_smokers",
    "binge_drinking",
    "obesity",
    "colon_cancer_screening_adults_age_50_colonoscopy",
    "selfreported_health_status_excellentvery_goodgood",
    "flu_shot_in_last_12_months_adults_ages_65_not_ageadjusted"
FROM "nyc-open-data-csut-3wpr"
