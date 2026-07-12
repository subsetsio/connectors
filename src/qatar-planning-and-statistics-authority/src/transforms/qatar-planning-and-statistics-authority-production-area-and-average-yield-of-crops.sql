-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "crop_group",
    "mjmw_lmhswl",
    "crop",
    "lmhswl",
    "production",
    "area",
    "yield"
FROM "qatar-planning-and-statistics-authority-production-area-and-average-yield-of-crops"
