-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "ljns",
    "willingness_to_work_in_private_sector",
    "lrgb_ll_ml_fy_lqt_lkhs",
    "value"
FROM "qatar-planning-and-statistics-authority-unemployed-qataris-15-years-and-above-by-gender-and-willingness-to-work-in-private-sector"
