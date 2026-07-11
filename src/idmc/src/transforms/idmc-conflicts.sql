-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the validated annual conflict and violence country-year series; do not combine it with the combined displacement totals without accounting for overlapping conflict measures.
SELECT
    "iso3",
    "country_name",
    "year",
    "new_displacement",
    "new_displacement_rounded",
    "total_displacement_rounded",
    "total_displacement"
FROM "idmc-conflicts"
