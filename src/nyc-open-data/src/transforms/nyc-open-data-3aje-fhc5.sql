-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "submission_time",
    "elected_officals_office_you_represent",
    "elected_officials_office_address",
    "elected_officals_email_address",
    "last_name_of_requestor",
    "first_name_of_requestor",
    "position_title_of_requestor",
    "email_address_of_requestor",
    "name_of_the_city_agency_you_are_requesting_to_engage",
    "additional_city_agency_you_are_requesting_to_engage"
FROM "nyc-open-data-3aje-fhc5"
