-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "73142",
    "Organization_Institution" AS organization_institution,
    "Effective_Date" AS effective_date
FROM "sg-data-d-2864c425e22ddb89969585820629adf8"
