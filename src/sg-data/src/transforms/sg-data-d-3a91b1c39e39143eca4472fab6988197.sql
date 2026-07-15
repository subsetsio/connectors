-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "donor-donee_relationship" AS donor_donee_relationship,
    "number_of_donees"
FROM "sg-data-d-3a91b1c39e39143eca4472fab6988197"
