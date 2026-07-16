-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BalanceSheetItemsProvinces" AS balancesheetitemsprovinces,
    "Regions" AS regions,
    "Periods" AS periods,
    "BalanceSheetItemsYearEndInMlnEuro_1" AS balancesheetitemsyearendinmlneuro_1,
    "BalanceSheetYearEndInEuroInhabit_2" AS balancesheetyearendineuroinhabit_2,
    "BalanceSheetItemsProvinces_label" AS balancesheetitemsprovinces_label,
    "Regions_label" AS regions_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-71536eng"
