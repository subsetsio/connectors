-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "as_of_date",
    "tax_id",
    "active_per_last_reported_status",
    "last_reported_active_date",
    "officer_first_name",
    "officer_last_name",
    "officer_race",
    "officer_gender",
    "current_rank_abbreviation",
    "current_rank",
    "current_command",
    "shield_no",
    "total_complaints",
    "total_substantiated_complaints"
FROM "nyc-open-data-2fir-qns4"
