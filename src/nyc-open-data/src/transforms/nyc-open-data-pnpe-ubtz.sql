-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "event_start_date",
    "event_start_time",
    "event_end_time",
    "borough",
    "zip_code",
    "primary_language",
    "list_of_languages",
    "total_attendees",
    "total_households_reporting_children",
    "number_of_people_receiving_inhouse_immigration_legal_referrals",
    "total_people_requesting_immigration_legal_referrals"
FROM "nyc-open-data-pnpe-ubtz"
