-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency_name",
    "address",
    "hours_monday",
    "hours_tuesday",
    "hours_wednesday",
    "hours_thursday",
    "hours_friday",
    "hours_saturday",
    "hours_sunday",
    "website",
    "phone_number",
    "borough",
    "zip_code",
    "ages_served",
    "special_population_served",
    "payment_cost",
    "free_self_tests",
    "additional_information"
FROM "nyc-open-data-72ss-25qh"
