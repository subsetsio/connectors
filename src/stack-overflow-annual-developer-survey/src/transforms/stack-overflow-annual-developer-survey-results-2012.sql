-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This early survey file does not expose a stable respondent identifier; treat rows as anonymized response records rather than joinable respondent entities.
-- caution: Question text, column names, coding, and multi-select answer encoding are specific to the 2012 questionnaire and are not harmonized to later years.
SELECT
    "What_Country_or_Region_do_you_live_in" AS what_country_or_region_do_you_live_in,
    "Which_US_State_or_Territory_do_you_live_in" AS which_us_state_or_territory_do_you_live_in,
    "How_old_are_you" AS how_old_are_you,
    "How_many_years_of_IT_Programming_experience_do_you_have" AS how_many_years_of_it_programming_experience_do_you_have,
    "How_would_you_best_describe_the_industry_you_currently_work_in" AS how_would_you_best_describe_the_industry_you_currently_work_in,
    "Which_best_describes_the_size_of_your_company" AS which_best_describes_the_size_of_your_company,
    "Which_of_the_following_best_describes_your_occupation" AS which_of_the_following_best_describes_your_occupation,
    "What_is_your_involvement_in_purchasing_products_or_services_for_the_company_you_work_for_You_can_choose_more_than_one" AS purchasing_involvement,
    "What_types_of_purchases_are_you_involved_in" AS what_types_of_purchases_are_you_involved_in,
    "What_is_your_budget_for_outside_expenditures_hardware_software_consulting_etc_for_2011" AS outside_expenditure_budget_2011,
    "What_type_of_project_are_you_developing" AS what_type_of_project_are_you_developing,
    "Which_languages_are_you_proficient_in" AS which_languages_are_you_proficient_in,
    "Unnamed_36" AS source_column_36,
    "Which_desktop_operating_system_do_you_use_the_most" AS which_desktop_operating_system_do_you_use_the_most,
    "What_best_describes_your_career_job_satisfaction" AS what_best_describes_your_career_job_satisfaction,
    "Including_bonus_what_is_your_annual_compensation_in_USD" AS including_bonus_what_is_your_annual_compensation_in_usd,
    "Have_you_visited_Are_you_aware_of_Stack_Overflow_Careers" AS have_you_visited_are_you_aware_of_stack_overflow_careers,
    "Do_you_have_a_Stack_Overflow_Careers_Profile" AS do_you_have_a_stack_overflow_careers_profile,
    "You_answered_you_don_t_have_a_Careers_profile_can_you_elaborate_why" AS career_profile_absence_reason,
    "Unnamed_43" AS source_column_43,
    "Which_technology_products_do_you_own_You_can_choose_more_than_one" AS technology_products_owned,
    "Unnamed_63" AS source_column_63,
    "In_the_last_12_months_how_much_money_have_you_spent_on_personal_technology_related_purchases" AS personal_tech_spend_last_12_months,
    "Please_rate_the_advertising_you_ve_seen_on_Stack_Overflow" AS please_rate_the_advertising_you_ve_seen_on_stack_overflow,
    "Unnamed_66" AS source_column_66,
    "Unnamed_67" AS source_column_67,
    "Unnamed_68" AS source_column_68,
    "Unnamed_69" AS source_column_69,
    "Unnamed_70" AS source_column_70,
    "What_advertisers_do_you_remember_seeing_on_Stack_Overflow" AS what_advertisers_do_you_remember_seeing_on_stack_overflow,
    "What_is_your_current_Stack_Overflow_reputation" AS what_is_your_current_stack_overflow_reputation,
    "Which_of_our_sites_do_you_frequent_most" AS which_of_our_sites_do_you_frequent_most,
    "Unnamed_74" AS source_column_74
FROM "stack-overflow-annual-developer-survey-results-2012"
