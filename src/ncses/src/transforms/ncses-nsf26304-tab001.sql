-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Fiscal year" AS fiscal_year,
    "All R and D expendituresa" AS all_r_and_d_expendituresa,
    "Source of funds - Federal government" AS source_of_funds_federal_government,
    "Source of funds - State and local government" AS source_of_funds_state_and_local_government,
    "Source of funds - Institution funds" AS source_of_funds_institution_funds,
    "Source of funds - Business" AS source_of_funds_business,
    "Source of funds - All other sourcesb" AS source_of_funds_all_other_sourcesb
FROM "ncses-nsf26304-tab001"
