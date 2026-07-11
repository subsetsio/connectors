-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "R and D and R and D plant expenditures" AS r_and_d_and_r_and_d_plant_expenditures,
    "R and D expendituresa" AS r_and_d_expendituresa,
    "R and D plant expendituresb" AS r_and_d_plant_expendituresb
FROM "ncses-nsf26302-tab001"
