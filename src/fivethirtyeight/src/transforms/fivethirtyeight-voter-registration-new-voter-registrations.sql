-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Jurisdiction" AS jurisdiction,
    "Year" AS year,
    "Month" AS month,
    "New registered voters" AS new_registered_voters
FROM "fivethirtyeight-voter-registration-new-voter-registrations"
