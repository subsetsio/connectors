-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "land_type",
    "stkhdm_l_rd",
    "crop",
    "lmhswl",
    "area"
FROM "qatar-planning-and-statistics-authority-land-utilization"
