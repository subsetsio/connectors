-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Graduate students - All fields" AS graduate_students_all_fields,
    "Graduate students - Science" AS graduate_students_science,
    "Graduate students - Engineering" AS graduate_students_engineering,
    "Graduate students - Health" AS graduate_students_health,
    "Postdoctoral appointees - All fields" AS postdoctoral_appointees_all_fields,
    "Postdoctoral appointees - Science" AS postdoctoral_appointees_science,
    "Postdoctoral appointees - Engineering" AS postdoctoral_appointees_engineering,
    "Postdoctoral appointees - Health" AS postdoctoral_appointees_health,
    "Doctorate-holding nonfaculty - All fields" AS doctorate_holding_nonfaculty_all_fields,
    "Doctorate-holding nonfaculty - Science" AS doctorate_holding_nonfaculty_science,
    "Doctorate-holding nonfaculty - Engineering" AS doctorate_holding_nonfaculty_engineering,
    "Doctorate-holding nonfaculty - Health" AS doctorate_holding_nonfaculty_health
FROM "ncses-nsf26307-tab001-001"
