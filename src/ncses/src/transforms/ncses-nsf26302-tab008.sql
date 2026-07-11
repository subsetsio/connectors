-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "All R and D expenditures" AS all_r_and_d_expenditures,
    "Agriculture" AS agriculture,
    "Energy" AS energy,
    "Environment and natural resources" AS environment_and_natural_resources,
    "Health" AS health,
    "Transportation" AS transportation,
    "Other R and D functionsa" AS other_r_and_d_functionsa
FROM "ncses-nsf26302-tab008"
