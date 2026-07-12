-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "certificate_type",
    "nw_lshhd",
    "total_number_of_certificates_issued"
FROM "qatar-planning-and-statistics-authority-total-certificates-issued-by-year-and-certificate-type"
