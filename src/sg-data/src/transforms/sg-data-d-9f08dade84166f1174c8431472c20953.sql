-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "source",
    "percentage_of_tax_deductible_donations"
FROM "sg-data-d-9f08dade84166f1174c8431472c20953"
