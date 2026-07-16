-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "TotalTechnologicalInnovators_1" AS totaltechnologicalinnovators_1,
    "AsOfThePopulation_2" AS asofthepopulation_2,
    "TotalTechnologicalInnovators_3" AS totaltechnologicalinnovators_3,
    "ProductInnovators_4" AS productinnovators_4,
    "ProcessInnovators_5" AS processinnovators_5,
    "InnovationCoOperation_6" AS innovationcooperation_6,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80066eng"
