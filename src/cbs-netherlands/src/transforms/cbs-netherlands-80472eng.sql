-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SIC2008SizeClasses" AS sic2008sizeclasses,
    "Periods" AS periods,
    "UnfilledVacancies_1" AS unfilledvacancies_1,
    "NewVacancies_2" AS newvacancies_2,
    "FilledVacancies_3" AS filledvacancies_3,
    "SIC2008SizeClasses_label" AS sic2008sizeclasses_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80472eng"
