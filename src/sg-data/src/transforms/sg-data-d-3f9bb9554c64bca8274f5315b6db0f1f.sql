-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "applicant_country",
    "patent_filings",
    "rank"
FROM "sg-data-d-3f9bb9554c64bca8274f5315b6db0f1f"
