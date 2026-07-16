-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AreasOfCivilEngineeringWorks" AS areasofcivilengineeringworks,
    "Periods" AS periods,
    "InputPriceIndex_1" AS inputpriceindex_1,
    "ChangesComparedWithOneYearEarlier_2" AS changescomparedwithoneyearearlier_2,
    "AreasOfCivilEngineeringWorks_label" AS areasofcivilengineeringworks_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-81139eng"
