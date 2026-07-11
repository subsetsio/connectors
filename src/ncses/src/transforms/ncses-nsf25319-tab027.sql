-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year of project start and type of institution" AS year_of_project_start_and_type_of_institution,
    "All sources" AS all_sources,
    "Government - Federal" AS government_federal,
    "Government - State and local" AS government_state_and_local,
    "Institutional funds and other sourcesa - State and local" AS institutional_funds_and_other_sourcesa_state_and_local
FROM "ncses-nsf25319-tab027"
