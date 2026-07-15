-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "applicant_country",
    "trademark_filings_classes",
    "rank"
FROM "sg-data-d-b21db8b17b4e4c11374abff3a09cb788"
