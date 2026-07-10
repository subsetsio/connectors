-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "growth_period",
    "province",
    "high_growth_enterprises",
    "employees_in_high_growth_enterprises"
FROM "statistics-austria-ogd-reg-hg-ab2008-hgud-ogd-1"
