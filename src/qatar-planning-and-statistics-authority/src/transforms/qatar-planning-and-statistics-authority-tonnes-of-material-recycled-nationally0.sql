-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "e_waste_collection_and_recycling_metrics",
    "value",
    "year"
FROM "qatar-planning-and-statistics-authority-tonnes-of-material-recycled-nationally0"
