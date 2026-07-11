-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Per-pupil expenditure rows include funding-source measures; compare like funding categories and reporting levels.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "pupil_count_tot",
    "federal_exp",
    "per_federal_exp",
    "state_local_exp",
    "per_state_local_exp",
    "fed_state_local_exp",
    "per_fed_state_local_exp",
    CAST("institution_id" AS BIGINT) AS institution_id,
    "data_reported_enr",
    "data_reported_exp"
FROM "new-york-state-education-department-src-expenditures-per-pupil"
