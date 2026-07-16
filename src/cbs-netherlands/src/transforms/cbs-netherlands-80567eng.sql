-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SIC2008" AS sic2008,
    "Periods" AS periods,
    "VacancyRate_1" AS vacancyrate_1,
    "SIC2008_label" AS sic2008_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80567eng"
