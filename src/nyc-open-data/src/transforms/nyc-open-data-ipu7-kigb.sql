-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zip_codes",
    "outreach_events",
    "general_outreach",
    "outreach_meetings",
    "educational_trainings",
    "fjc",
    "undesignated",
    "civic_service_agencies",
    "education_agencies",
    "health_agencies",
    "nycha",
    "public_safety_agencies",
    "social_service_agencies",
    "cbos",
    "house_of_worship",
    "consulates",
    "outreach_partner_not_noted",
    "total_population",
    "population_poverty_status_determined",
    "of_residents_living_below_poverty",
    "number_residents_foreignborn",
    "residents_foreign_born",
    "residents_speak_english_less_than_very_well",
    "of_residents_black_or_african_american",
    "residents_hispanic_or_latino",
    "precinct",
    "dirs_2018",
    "dir_2019",
    "fjc_clients"
FROM "nyc-open-data-ipu7-kigb"
