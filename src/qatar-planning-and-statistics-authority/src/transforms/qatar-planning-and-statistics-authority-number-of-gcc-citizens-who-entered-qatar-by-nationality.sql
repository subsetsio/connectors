-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "nationality_ar",
    "2018_entry",
    "2018_exit",
    "2019_entry",
    "2019_exit",
    "2020_entry",
    "2020_exit",
    "2021_entry",
    "2021_exit",
    "2022_entry",
    "2022_exit",
    "2023_entry",
    "2023_exit"
FROM "qatar-planning-and-statistics-authority-number-of-gcc-citizens-who-entered-qatar-by-nationality"
