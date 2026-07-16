-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BalanceSheetItemsMunicipalities" AS balancesheetitemsmunicipalities,
    "Regions" AS regions,
    "Periods" AS periods,
    "BalanceSheetItemsYearEndInMlnEuro_1" AS balancesheetitemsyearendinmlneuro_1,
    "BalanceSheetYearEndInEuroInhabit_2" AS balancesheetyearendineuroinhabit_2,
    "BalanceSheetItemsMunicipalities_label" AS balancesheetitemsmunicipalities_label,
    "Regions_label" AS regions_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-71231eng"
