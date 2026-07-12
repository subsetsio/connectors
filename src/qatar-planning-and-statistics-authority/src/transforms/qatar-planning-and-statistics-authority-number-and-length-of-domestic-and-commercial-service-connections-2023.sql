-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_service",
    "nw_lkhdm",
    "15mm_length",
    "15mm_nos",
    "22mm_length",
    "22_mm_nos",
    "28_mm_length",
    "28_mm_nos",
    "42_mm_length",
    "42_mm_nos",
    "54_mm_length",
    "54_mm_nos",
    "total_length",
    "total_nos"
FROM "qatar-planning-and-statistics-authority-number-and-length-of-domestic-and-commercial-service-connections-2023"
