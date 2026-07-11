-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "All intramural R and D expenditures" AS all_intramural_r_and_d_expenditures,
    "Type of R and D - Basic research" AS type_of_r_and_d_basic_research,
    "Type of R and D - Applied research" AS type_of_r_and_d_applied_research,
    "Type of R and D - Experimental development" AS type_of_r_and_d_experimental_development
FROM "ncses-nsf26302-tab007"
