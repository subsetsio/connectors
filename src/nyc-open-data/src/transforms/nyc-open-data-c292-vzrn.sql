-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "opened_on",
    "topic",
    "industry",
    "status",
    "completed_on",
    "outcome_activity",
    "civil_penalties_assessed",
    "total_number_of_employees_awarded_restitution",
    "total_amount_of_restitution_awarded",
    "city",
    "state",
    "postal_code",
    "borough_name",
    "community_district",
    "council_district"
FROM "nyc-open-data-c292-vzrn"
