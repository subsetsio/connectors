-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All engineering fields" AS all_engineering_fields,
    "Aerospace aeronautical astronautical and space engineering" AS aerospace_aeronautical_astronautical_and_space_engineering,
    "Biological biomedical and biosystems engineering" AS biological_biomedical_and_biosystems_engineering,
    "Chemical and petroleum engineering" AS chemical_and_petroleum_engineering,
    "Civil environmental and transportation engineering" AS civil_environmental_and_transportation_engineering,
    "Electrical and computer engineering" AS electrical_and_computer_engineering,
    "Engineering technologies" AS engineering_technologies,
    "Industrial engineering and operations research" AS industrial_engineering_and_operations_research,
    "Materials and mining engineering" AS materials_and_mining_engineering,
    "Mechanical engineering" AS mechanical_engineering,
    "Engineering other" AS engineering_other
FROM "ncses-nsf25349-tab008-006"
