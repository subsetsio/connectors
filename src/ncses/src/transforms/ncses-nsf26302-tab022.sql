-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "R and D personnel headcount - Total" AS r_and_d_personnel_headcount_total,
    "R and D personnel headcount - Researchersa" AS r_and_d_personnel_headcount_researchersa,
    "R and D personnel headcount - Technicians" AS r_and_d_personnel_headcount_technicians,
    "R and D personnel headcount - Support staff" AS r_and_d_personnel_headcount_support_staff,
    "R and D personnel full-time equivalent - Total" AS r_and_d_personnel_full_time_equivalent_total,
    "R and D personnel full-time equivalent - Researchersa" AS r_and_d_personnel_full_time_equivalent_researchersa,
    "R and D personnel full-time equivalent - Technicians" AS r_and_d_personnel_full_time_equivalent_technicians,
    "R and D personnel full-time equivalent - Support staff" AS r_and_d_personnel_full_time_equivalent_support_staff
FROM "ncses-nsf26302-tab022"
