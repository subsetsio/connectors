-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "agency",
    "construction_count",
    "construction_contract_value",
    "project_labor_agreement_count",
    "project_labor_agreement_contract_value",
    "apprenticeship_program_directive_count",
    "apprenticeship_program_directive_contract_value"
FROM "nyc-open-data-6w36-zfn5"
