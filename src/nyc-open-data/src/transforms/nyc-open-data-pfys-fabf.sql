-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borocentral_library",
    "network",
    "branch",
    "adult_program",
    "adult_attendance",
    "young_adult_program",
    "young_adult_attendance",
    "juvenile_program",
    "juvenile_attendance",
    "outreach_services_program",
    "outreach_services_attendance",
    "total_program",
    "total_attendance",
    "reference_transactions_adult",
    "reference_transactions_young_adult",
    "reference_transactions_juvenile",
    "reference_transactions",
    "circulation_adult",
    "circulation_young_adult",
    "circulation_juvenile",
    "circulation",
    "weekly_hours_of_public_service"
FROM "nyc-open-data-pfys-fabf"
