-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "total_waste_recycled_tons",
    "non_hazardous_waste_generated_tons",
    "hazardous_waste_generated_tons"
FROM "qatar-planning-and-statistics-authority-total-waste-generated-by-type-and-recycled"
