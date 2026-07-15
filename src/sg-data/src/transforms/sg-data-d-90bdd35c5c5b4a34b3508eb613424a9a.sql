-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "energy_produced_from_inc"
FROM "sg-data-d-90bdd35c5c5b4a34b3508eb613424a9a"
