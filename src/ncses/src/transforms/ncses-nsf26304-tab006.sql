-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "Total - 2021" AS total_2021,
    "Total - 2022" AS total_2022,
    "Total - 2023" AS total_2023,
    "Total - 2024" AS total_2024,
    "Federally financed - 2021" AS federally_financed_2021,
    "Federally financed - 2022" AS federally_financed_2022,
    "Federally financed - 2023" AS federally_financed_2023,
    "Federally financed - 2024" AS federally_financed_2024
FROM "ncses-nsf26304-tab006"
