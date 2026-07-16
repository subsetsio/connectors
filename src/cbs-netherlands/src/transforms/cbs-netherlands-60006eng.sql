-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "TheoreticallyAvailableHours_1" AS theoreticallyavailablehours_1,
    "TotalNonProductiveHours_2" AS totalnonproductivehours_2,
    "FrostAndPrecipitationDelays_3" AS frostandprecipitationdelays_3,
    "Other_4" AS other_4,
    "ProductiveHours_5" AS productivehours_5,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-60006eng"
