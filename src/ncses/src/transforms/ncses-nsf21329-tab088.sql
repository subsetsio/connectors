-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State or location" AS state_or_location,
    "Total" AS total,
    "R and D" AS r_and_d,
    "R and D plant" AS r_and_d_plant
FROM "ncses-nsf21329-tab088"
