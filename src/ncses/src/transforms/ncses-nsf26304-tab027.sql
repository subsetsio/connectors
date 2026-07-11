-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State institutional control and institution" AS state_institutional_control_and_institution,
    "All personnel functions - Headcount" AS all_personnel_functions_headcount,
    "All personnel functions - FTEs" AS all_personnel_functions_ftes,
    "All personnel functions - FTEs_2" AS all_personnel_functions_ftes_2,
    "Researchers - Headcount" AS researchers_headcount,
    "Researchers - FTEs" AS researchers_ftes,
    "Researchers - FTEs_2" AS researchers_ftes_2,
    "R and D technicians - Headcount" AS r_and_d_technicians_headcount,
    "R and D technicians - FTEs" AS r_and_d_technicians_ftes,
    "R and D technicians - FTEs_2" AS r_and_d_technicians_ftes_2,
    "R and D support staff - Headcount" AS r_and_d_support_staff_headcount,
    "R and D support staff - FTEs" AS r_and_d_support_staff_ftes,
    "R and D support staff - FTEs_2" AS r_and_d_support_staff_ftes_2
FROM "ncses-nsf26304-tab027"
