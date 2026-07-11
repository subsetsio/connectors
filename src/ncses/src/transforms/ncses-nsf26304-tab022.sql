-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "2022",
    "2023",
    "2024 - All engineering" AS 2024_all_engineering,
    "2024 - Aerospace aeronautical and astronautical engineering" AS 2024_aerospace_aeronautical_and_astronautical_engineering,
    "2024 - Bioengineering and biomedical engineering" AS 2024_bioengineering_and_biomedical_engineering,
    "2024 - Chemical engineering" AS 2024_chemical_engineering,
    "2024 - Civil engineering" AS 2024_civil_engineering,
    "2024 - Electrical electronic and communications engineering" AS 2024_electrical_electronic_and_communications_engineering,
    "2024 - Industrial and manufacturing engineering" AS 2024_industrial_and_manufacturing_engineering,
    "2024 - Mechanical engineering" AS 2024_mechanical_engineering,
    "2024 - Metallurgical and materials engineering" AS 2024_metallurgical_and_materials_engineering,
    "2024 - Engineering nec" AS 2024_engineering_nec
FROM "ncses-nsf26304-tab022"
