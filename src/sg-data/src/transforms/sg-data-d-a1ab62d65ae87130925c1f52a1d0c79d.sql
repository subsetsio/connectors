-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "condition",
    "percentage_diagnoses"
FROM "sg-data-d-a1ab62d65ae87130925c1f52a1d0c79d"
