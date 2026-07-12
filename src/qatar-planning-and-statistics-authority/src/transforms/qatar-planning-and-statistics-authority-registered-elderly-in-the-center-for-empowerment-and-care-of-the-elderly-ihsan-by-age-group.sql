-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group",
    "nationality",
    "gender",
    "lfy_l_mry",
    "ljnsy",
    "lnw",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-elderly-in-the-center-for-empowerment-and-care-of-the-elderly-ihsan-by-age-group"
