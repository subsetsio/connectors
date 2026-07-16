-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SIC2008PrivateFirmsGovernment" AS sic2008privatefirmsgovernment,
    "Periods" AS periods,
    "VacanciesSeasonallyAdjusted_1" AS vacanciesseasonallyadjusted_1,
    "SIC2008PrivateFirmsGovernment_label" AS sic2008privatefirmsgovernment_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80474eng"
