-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "start_of_period",
    "end_of_period",
    "gender",
    "type_of_cancer",
    "incidence_rate",
    "rank"
FROM "sg-data-d-c375edebfa33e2ac0e29469a4755fc97"
