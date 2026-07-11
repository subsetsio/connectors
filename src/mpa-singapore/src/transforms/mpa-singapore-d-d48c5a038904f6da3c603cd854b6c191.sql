-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "number_of_vessels",
    "gross_tonnage"
FROM "mpa-singapore-d-d48c5a038904f6da3c603cd854b6c191"
