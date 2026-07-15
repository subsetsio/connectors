-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_type",
    "financial_scheme",
    "eligibility",
    "award_quantum_conditions",
    "reference"
FROM "sg-data-d-5711f5307bc216e7588b768cd9ad6dae"
