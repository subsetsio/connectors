-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "mainland_state_owned_entities",
    "mainland_private_entities",
    "non-mainland_entities" AS non_mainland_entities,
    "lending_total"
FROM "hkma-mainland-lending-borrowers-type"
