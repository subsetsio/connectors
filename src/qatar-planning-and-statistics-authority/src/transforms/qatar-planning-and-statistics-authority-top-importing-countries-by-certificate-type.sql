-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "certificate_type",
    "nw_lshhd",
    "top_importing_country",
    "ldwl_lmstwrd_l_l",
    "number_of_certificates_issued",
    "percentage_of_the_country_s_share_of_total_certificates_for_that_type"
FROM "qatar-planning-and-statistics-authority-top-importing-countries-by-certificate-type"
