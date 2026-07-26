-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "borough",
    "number_salons_visited",
    "number_materials_distributed",
    "cosmetologist_trainings_provided",
    "number_cosmetologist_trained",
    "cosmetologist_toolkit_downloads"
FROM "nyc-open-data-mpbx-6c9k"
