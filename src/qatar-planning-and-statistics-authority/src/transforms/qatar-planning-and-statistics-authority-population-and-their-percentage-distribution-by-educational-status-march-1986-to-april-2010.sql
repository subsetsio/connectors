-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_status",
    "lhl_lt_lymy",
    "number_march_1986",
    "percentage_march_1986",
    "number_march_1997",
    "percentage_march_1997",
    "number_march_2004",
    "percentage_march_2004",
    "number_april_2010",
    "percentage_april_2010"
FROM "qatar-planning-and-statistics-authority-population-and-their-percentage-distribution-by-educational-status-march-1986-to-april-2010"
