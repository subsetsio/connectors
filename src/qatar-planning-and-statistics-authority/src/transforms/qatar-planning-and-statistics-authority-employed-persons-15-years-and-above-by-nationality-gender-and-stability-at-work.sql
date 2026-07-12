-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "stability_at_work",
    "lstqrr_fy_l_ml",
    "value"
FROM "qatar-planning-and-statistics-authority-employed-persons-15-years-and-above-by-nationality-gender-and-stability-at-work"
