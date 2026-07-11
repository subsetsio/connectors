-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "chamber_code",
    "parliament",
    "chamber_name",
    "chamber_name_full",
    "struct_parl_status",
    "designation_mode",
    "electoral_system",
    "current_members_number",
    "current_men_number",
    "current_women_number",
    "current_women_percent",
    "statutory_members_number",
    "directly_elected_number",
    "age_average",
    "total_younger_30_percentage",
    "total_younger_40_percentage",
    "total_younger_45_percentage",
    "total_older_46_percentage",
    "female_younger_45_percentage",
    "gender_quota_or_reserved_seats",
    "youth_quota_or_reserved_seats",
    "is_electoral_quota_women",
    "min_age_member_parl",
    "min_age_vote_elect",
    "basic_salary",
    "num_cham_perm_committees",
    "groups_number",
    "permanent_staff_number",
    "parliamentary_term",
    "num_days_parl_plen",
    "last_election",
    "num_written_question_ask",
    "num_written_question_answ"
FROM "inter-parliamentary-union-chambers"
