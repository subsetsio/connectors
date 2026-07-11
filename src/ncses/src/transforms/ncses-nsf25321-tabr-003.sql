-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "Working after retirement - Total" AS working_after_retirement_total,
    "Working after retirement - SE" AS working_after_retirement_se,
    "Reasons for working after retiring - Wanted a professional identity - Percent" AS reasons_for_working_after_retiring_wanted_a_professional_identity_percent,
    "Reasons for working after retiring - Wanted a professional identity - SE" AS reasons_for_working_after_retiring_wanted_a_professional_identity_se,
    "Reasons for working after retiring - Wanted additional income - Percent" AS reasons_for_working_after_retiring_wanted_additional_income_percent,
    "Reasons for working after retiring - Wanted additional income - SE" AS reasons_for_working_after_retiring_wanted_additional_income_se,
    "Reasons for working after retiring - Wanted social connection - Percent" AS reasons_for_working_after_retiring_wanted_social_connection_percent,
    "Reasons for working after retiring - Wanted social connection - SE" AS reasons_for_working_after_retiring_wanted_social_connection_se,
    "Reasons for working after retiring - Was asked to continue or return to work - Percent" AS reasons_for_working_after_retiring_was_asked_to_continue_or_return_to_work_percent,
    "Reasons for working after retiring - Was asked to continue or return to work - SE" AS reasons_for_working_after_retiring_was_asked_to_continue_or_return_to_work_se,
    "Reasons for working after retiring - Needed additional income - Percent" AS reasons_for_working_after_retiring_needed_additional_income_percent,
    "Reasons for working after retiring - Needed additional income - SE" AS reasons_for_working_after_retiring_needed_additional_income_se,
    "Reasons for working after retiring - Health insurancea - Percent" AS reasons_for_working_after_retiring_health_insurancea_percent,
    "Reasons for working after retiring - Health insurancea - SE" AS reasons_for_working_after_retiring_health_insurancea_se,
    "Reasons for working after retiring - Other reasonsb - Percent" AS reasons_for_working_after_retiring_other_reasonsb_percent,
    "Reasons for working after retiring - Other reasonsb - SE" AS reasons_for_working_after_retiring_other_reasonsb_se
FROM "ncses-nsf25321-tabr-003"
