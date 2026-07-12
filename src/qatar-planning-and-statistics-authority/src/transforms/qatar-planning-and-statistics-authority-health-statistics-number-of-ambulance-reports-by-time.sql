-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "00_01_06_00",
    "06_01_12_00",
    "12_01_18_00",
    "18_01_24_00"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-ambulance-reports-by-time"
