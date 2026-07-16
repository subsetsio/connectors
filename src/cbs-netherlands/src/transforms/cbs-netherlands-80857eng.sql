-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GovernmentSectors" AS governmentsectors,
    "Periods" AS periods,
    "UnfilledVacancies_1" AS unfilledvacancies_1,
    "NewVacancies_2" AS newvacancies_2,
    "FilledVacancies_3" AS filledvacancies_3,
    "GovernmentSectors_label" AS governmentsectors_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80857eng"
