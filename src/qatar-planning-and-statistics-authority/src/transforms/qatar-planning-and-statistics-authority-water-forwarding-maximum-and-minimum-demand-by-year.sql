-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "average_forwarding_migd",
    "maximum_forwarding_migd",
    "maximum_forwarding_month",
    "shhr_l_qs",
    "minimum_forwarding_migd",
    "minimum_forwarding_month",
    "shhr_l_dn"
FROM "qatar-planning-and-statistics-authority-water-forwarding-maximum-and-minimum-demand-by-year"
