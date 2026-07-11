-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of highest degree and employment sector" AS field_of_highest_degree_and_employment_sector,
    "Number" AS number,
    "Salary" AS salary,
    "Primary work activity - Computer applications - Number" AS primary_work_activity_computer_applications_number,
    "Primary work activity - Computer applications - Salary" AS primary_work_activity_computer_applications_salary,
    "Primary work activity - Designa - Number" AS primary_work_activity_designa_number,
    "Primary work activity - Designa - Salary" AS primary_work_activity_designa_salary,
    "Primary work activity - Management and administrationb - Number" AS primary_work_activity_management_and_administrationb_number,
    "Primary work activity - Management and administrationb - Salary" AS primary_work_activity_management_and_administrationb_salary,
    "Primary work activity - Research and developmentc - Number" AS primary_work_activity_research_and_developmentc_number,
    "Primary work activity - Research and developmentc - Salary" AS primary_work_activity_research_and_developmentc_salary,
    "Primary work activity - Teaching - Number" AS primary_work_activity_teaching_number,
    "Primary work activity - Teaching - Salary" AS primary_work_activity_teaching_salary,
    "Primary work activity - Otherd - Number" AS primary_work_activity_otherd_number,
    "Primary work activity - Otherd - Salary" AS primary_work_activity_otherd_salary
FROM "ncses-nsf25322-tab004-003"
