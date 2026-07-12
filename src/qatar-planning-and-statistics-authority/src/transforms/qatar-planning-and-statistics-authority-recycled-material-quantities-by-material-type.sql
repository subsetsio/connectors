-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "material_type",
    "material_description",
    "total_tons",
    "recycled_tons",
    "recycled"
FROM "qatar-planning-and-statistics-authority-recycled-material-quantities-by-material-type"
