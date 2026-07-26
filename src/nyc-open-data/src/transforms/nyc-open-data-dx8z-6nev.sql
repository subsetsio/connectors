-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_donation",
    "organization_name",
    "donation_id",
    "donor_name",
    "donors_city_of_residence",
    "donors_state_of_residence",
    "moneyinkind_donation",
    "donation_value",
    "date_of_donation",
    "description_of_inkind_donation",
    "elected_official",
    "restricted_or_unrestricted"
FROM "nyc-open-data-dx8z-6nev"
