-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sub_indicator",
    "lmw_shr_lfr_y",
    "unit",
    "lwhd",
    "value",
    "year"
FROM "qatar-planning-and-statistics-authority-proportion-of-important-sites-for-terrestrial-and-freshwater-biodiversity-covered-by-protected-areas0"
