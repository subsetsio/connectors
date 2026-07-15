-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "highest_qualification",
    "duration_of_unemployment",
    "unemployed"
FROM "sg-data-d-e86bfae75632429f22fb315adba3e1a3"
