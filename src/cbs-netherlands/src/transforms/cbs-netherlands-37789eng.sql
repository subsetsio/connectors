-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "TotalNumberOfDisablementBenefits_1" AS totalnumberofdisablementbenefits_1,
    "BenefitsWAO_2" AS benefitswao_2,
    "BenefitsWajong_3" AS benefitswajong_3,
    "BenefitsWAZ_4" AS benefitswaz_4,
    "TotalBenefitsWIA_5" AS totalbenefitswia_5,
    "BenefitsIVA_6" AS benefitsiva_6,
    "BenefitsWGA_7" AS benefitswga_7,
    "BenefitsWWNotSeasonallyAdjusted_8" AS benefitswwnotseasonallyadjusted_8,
    "BenefitsWWSeasonallyAdjusted_9" AS benefitswwseasonallyadjusted_9,
    "BenefitsIOW_10" AS benefitsiow_10,
    "TotalBenefitsIncomeSupport_11" AS totalbenefitsincomesupport_11,
    "BenefitsIncomeSupportUpToAOWAge_12" AS benefitsincomesupportuptoaowage_12,
    "BenefitsIncomeSupportFromAOWAge_13" AS benefitsincomesupportfromaowage_13,
    "BenefitsIOAW_14" AS benefitsioaw_14,
    "BenefitsIOAZ_15" AS benefitsioaz_15,
    "BenefitsAOW_16" AS benefitsaow_16,
    "BenefitsAnw_17" AS benefitsanw_17,
    "PersonsEntitledToAKW_18" AS personsentitledtoakw_18,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-37789eng"
