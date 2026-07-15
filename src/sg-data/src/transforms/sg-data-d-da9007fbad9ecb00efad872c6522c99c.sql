-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "applicant_country",
    "design_filings",
    "rank"
FROM "sg-data-d-da9007fbad9ecb00efad872c6522c99c"
