-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This early survey file does not expose a stable respondent identifier; treat rows as anonymized response records rather than joinable respondent entities.
-- caution: Question text, column names, coding, and multi-select answer encoding are specific to the 2011 questionnaire and are not harmonized to later years.
SELECT
    "What_Country_or_Region_do_you_live_in" AS what_country_or_region_do_you_live_in,
    "Which_US_State_or_Territory_do_you_live_in" AS which_us_state_or_territory_do_you_live_in,
    "How_old_are_you" AS how_old_are_you,
    "How_many_years_of_IT_Programming_experience_do_you_have" AS how_many_years_of_it_programming_experience_do_you_have,
    "How_would_you_best_describe_the_industry_you_work_in" AS how_would_you_best_describe_the_industry_you_work_in,
    "Which_best_describes_the_size_of_your_company" AS which_best_describes_the_size_of_your_company,
    "Which_of_the_following_best_describes_your_occupation" AS which_of_the_following_best_describes_your_occupation,
    "How_likely_is_it_that_a_recommendation_you_make_will_be_acted_upon" AS recommendation_action_likelihood,
    "What_is_your_involvement_in_purchasing_You_can_choose_more_than_1" AS purchasing_involvement,
    "What_types_of_purchases_are_you_involved_in" AS what_types_of_purchases_are_you_involved_in,
    "What_is_your_budget_for_outside_expenditures_hardware_software_consulting_etc_for_2011" AS outside_expenditure_budget_2011,
    "What_type_of_project_are_you_developing" AS what_type_of_project_are_you_developing,
    "Which_languages_are_you_proficient_in" AS which_languages_are_you_proficient_in,
    "Unnamed_42" AS source_column_42,
    "What_operating_system_do_you_use_the_most" AS what_operating_system_do_you_use_the_most,
    "Please_rate_your_job_career_satisfaction" AS please_rate_your_job_career_satisfaction,
    "Including_bonus_what_is_your_annual_compensation_in_USD" AS including_bonus_what_is_your_annual_compensation_in_usd,
    "Which_technology_products_do_you_own_You_can_choose_more_than_one" AS technology_products_owned,
    "Unnamed_62" AS source_column_62,
    "In_the_last_12_months_how_much_money_have_you_spent_on_personal_technology_related_purchases" AS personal_tech_spend_last_12_months,
    "Which_of_our_sites_do_you_frequent_most" AS which_of_our_sites_do_you_frequent_most
FROM "stack-overflow-annual-developer-survey-results-2011"
