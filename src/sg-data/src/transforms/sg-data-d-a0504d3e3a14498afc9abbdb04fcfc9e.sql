-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_computer",
    "computer_access_at_home"
FROM "sg-data-d-a0504d3e3a14498afc9abbdb04fcfc9e"
