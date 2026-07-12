-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_service",
    "nw_lkhdm",
    "80_mm_length",
    "80_mm_nos",
    "100_mm_length",
    "100_mm_nos",
    "150_mm_length",
    "150_mm_nos",
    "200_mm_length",
    "200_mm_nos",
    "250_mm_length",
    "250_mm_nos",
    "300_mm_length",
    "300_mm_nos",
    "400_mm_length",
    "400_mm_nos",
    "total_length",
    "total_nos"
FROM "qatar-planning-and-statistics-authority-number-and-length-of-bulk-service-connections-2023"
