-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Aeronautical engineering" AS aeronautical_engineering,
    "Astronautical engineering" AS astronautical_engineering,
    "Chemical engineering" AS chemical_engineering,
    "Civil engineering" AS civil_engineering,
    "Electrical engineering" AS electrical_engineering,
    "Mechanical engineering" AS mechanical_engineering,
    "Metallurgy and materials engineering" AS metallurgy_and_materials_engineering,
    "Other engineering" AS other_engineering
FROM "ncses-nsf21329-tab045"
