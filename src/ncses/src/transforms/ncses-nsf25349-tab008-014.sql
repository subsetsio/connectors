-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All education fields" AS all_education_fields,
    "Education leadership and administration" AS education_leadership_and_administration,
    "Education research" AS education_research,
    "Teacher education and teaching fields" AS teacher_education_and_teaching_fields,
    "Education other" AS education_other
FROM "ncses-nsf25349-tab008-014"
