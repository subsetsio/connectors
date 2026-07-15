-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_by_main_offence_group",
    "number_of_population"
FROM "sg-data-d-18077ea3d5e77ee03558d4f5b3b6683f"
