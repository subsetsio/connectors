-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_by_main_offence_group",
    "number_of_population"
FROM "sg-data-d-4da5f27c66f2967763aa5729e3d373b2"
