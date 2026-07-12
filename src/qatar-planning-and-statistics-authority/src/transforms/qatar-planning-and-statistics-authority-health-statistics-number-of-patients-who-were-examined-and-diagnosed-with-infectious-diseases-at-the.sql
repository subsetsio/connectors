-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "aids",
    "hepatitis_b",
    "hepatitis_c",
    "pulmonary_tuberculosis",
    "syphilis",
    "other"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-patients-who-were-examined-and-diagnosed-with-infectious-diseases-at-the"
