-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "certificate_type",
    "nw_lshhd",
    "importing_country",
    "ldwl_lmstwrd",
    "number_of_issued_certificates"
FROM "qatar-planning-and-statistics-authority-annual-certificates-of-origin-by-type-and-importing-country-open-access-data"
