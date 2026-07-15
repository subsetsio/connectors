-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "registration_no",
    "name",
    "business_address",
    "home_economy_or_jurisdiction_in_which_registered",
    "any_other_economy_in_which_registered",
    "offers_of_professional_alliance_from_other_apec_architects"
FROM "sg-data-d-65f6a92f8902a09caf2256855d3de376"
