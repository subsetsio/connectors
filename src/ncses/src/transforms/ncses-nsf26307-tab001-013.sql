-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Total" AS total,
    "Fellowships - Number" AS fellowships_number,
    "Fellowships - Percent" AS fellowships_percent,
    "Research assistantships - Number" AS research_assistantships_number,
    "Research assistantships - Percent" AS research_assistantships_percent,
    "Teaching assistantships - Number" AS teaching_assistantships_number,
    "Teaching assistantships - Percent" AS teaching_assistantships_percent,
    "Traineeships - Number" AS traineeships_number,
    "Traineeships - Percent" AS traineeships_percent,
    "Other types of support - Self-support - Number" AS other_types_of_support_self_support_number,
    "Other types of support - Self-support - Percent" AS other_types_of_support_self_support_percent,
    "Other types of support - Other - Number" AS other_types_of_support_other_number,
    "Other types of support - Other - Percent" AS other_types_of_support_other_percent
FROM "ncses-nsf26307-tab001-013"
