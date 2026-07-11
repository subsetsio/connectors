-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Level of highest degree and occupation" AS level_of_highest_degree_and_occupation,
    "Total" AS total,
    "Primary work activity - Computer applications" AS primary_work_activity_computer_applications,
    "Primary work activity - Designa" AS primary_work_activity_designa,
    "Primary work activity - Management and administrationb" AS primary_work_activity_management_and_administrationb,
    "Primary work activity - Research and developmentc" AS primary_work_activity_research_and_developmentc,
    "Primary work activity - Teaching" AS primary_work_activity_teaching,
    "Primary work activity - Otherd" AS primary_work_activity_otherd
FROM "ncses-nsf25322-tab003-001"
