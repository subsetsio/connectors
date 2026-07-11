-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This wide country-year table combines conflict and disaster measures; avoid summing it together with the separate conflict or disaster tables.
SELECT
    "iso3",
    "country_name",
    "year",
    "conflict_new_displacement",
    "conflict_new_displacement_rounded",
    "conflict_total_displacement",
    "conflict_total_displacement_rounded",
    "disaster_new_displacement",
    "disaster_new_displacement_rounded",
    "disaster_total_displacement",
    "disaster_total_displacement_rounded"
FROM "idmc-displacements"
