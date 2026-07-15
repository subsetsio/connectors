-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "mother_race",
    "place_of_birth",
    "birth_count"
FROM "sg-data-d-01e099752f815ec8979684630de92788"
