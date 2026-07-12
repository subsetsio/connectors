-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "establishments_by_number_of_employees",
    "lmnshat_hsb_dd_lmshtglyn",
    "category",
    "fy",
    "sub_category",
    "lfy_lfr_y",
    "lwhd",
    "value"
FROM "qatar-planning-and-statistics-authority-establishments-employees-and-compensations-of-employees-in-transport-and-communication-sector-by-size-of-establishment"
