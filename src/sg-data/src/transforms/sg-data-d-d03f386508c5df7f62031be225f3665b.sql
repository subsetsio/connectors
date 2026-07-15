-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Financial_Type" AS financial_type,
    "Financial_Scheme" AS financial_scheme,
    "Eligibility" AS eligibility,
    "Award_Quantum_and_Conditions" AS award_quantum_and_conditions,
    "Reference" AS reference
FROM "sg-data-d-d03f386508c5df7f62031be225f3665b"
