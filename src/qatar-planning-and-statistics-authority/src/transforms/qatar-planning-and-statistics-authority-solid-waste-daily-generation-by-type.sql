-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "domestic",
    "construction",
    "bulky",
    "tires",
    "others",
    "per_capita_domestic_waste_generation_kg_day",
    "total"
FROM "qatar-planning-and-statistics-authority-solid-waste-daily-generation-by-type"
