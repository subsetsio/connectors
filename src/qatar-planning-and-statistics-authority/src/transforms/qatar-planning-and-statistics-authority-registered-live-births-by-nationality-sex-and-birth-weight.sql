-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "birth_weight_grams",
    "lwzn_wqt_lwld",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-nationality-sex-and-birth-weight"
