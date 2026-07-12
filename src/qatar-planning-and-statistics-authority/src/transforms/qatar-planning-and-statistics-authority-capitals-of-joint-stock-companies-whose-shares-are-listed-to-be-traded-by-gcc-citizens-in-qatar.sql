-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "capitalization_million_qatari_riyals"
FROM "qatar-planning-and-statistics-authority-capitals-of-joint-stock-companies-whose-shares-are-listed-to-be-traded-by-gcc-citizens-in-qatar"
