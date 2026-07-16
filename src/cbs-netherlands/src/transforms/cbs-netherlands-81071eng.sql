-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "Ages" AS ages,
    "MedicineGroupATC" AS medicinegroupatc,
    "Periods" AS periods,
    "PersonsWithDispensedMedicines_1" AS personswithdispensedmedicines_1,
    "PersonsWithMedicinesRelative_2" AS personswithmedicinesrelative_2,
    "DefinedDailyDosesDDD_3" AS defineddailydosesddd_3,
    "DefinedDailyDosesDDDRelative_4" AS defineddailydosesdddrelative_4,
    "Sex_label" AS sex_label,
    "Ages_label" AS ages_label,
    "MedicineGroupATC_label" AS medicinegroupatc_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-81071eng"
