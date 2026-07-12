-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sub_indicator",
    "lmw_shr_lfr_y",
    "unit",
    "whd",
    "value",
    "year"
FROM "qatar-planning-and-statistics-authority-progress-towards-sustainable-forest-management0"
