-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BalanceSheetItemsWaterBoards" AS balancesheetitemswaterboards,
    "WaterBoards" AS waterboards,
    "Periods" AS periods,
    "BalanceSheetItemsAtYearEnd_1" AS balancesheetitemsatyearend_1,
    "BalanceSheetItemsWaterBoards_label" AS balancesheetitemswaterboards_label,
    "WaterBoards_label" AS waterboards_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80445eng"
