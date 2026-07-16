-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SexOfEmployee" AS sexofemployee,
    "TypeOfEmploymentContract" AS typeofemploymentcontract,
    "CaoSector" AS caosector,
    "JobCharacteristics" AS jobcharacteristics,
    "Periods" AS periods,
    "Jobs_1" AS jobs_1,
    "LabourVolume_2" AS labourvolume_2,
    "HourlyWage_3" AS hourlywage_3,
    "MonthlyWageIncludingOvertime_4" AS monthlywageincludingovertime_4,
    "MonthlyWageExcludingOvertime_5" AS monthlywageexcludingovertime_5,
    "YearlyWageIncludingBonuses_6" AS yearlywageincludingbonuses_6,
    "YearlyWageExcludingSpecialPayments_7" AS yearlywageexcludingspecialpayments_7,
    "BonusesAndAllowances_8" AS bonusesandallowances_8,
    "AdditionalTaxLiabilityForCompanyCar_9" AS additionaltaxliabilityforcompanycar_9,
    "PerJobPerWeekIncludingOvertime_10" AS perjobperweekincludingovertime_10,
    "PerJobPerWeekExcludingOvertime_11" AS perjobperweekexcludingovertime_11,
    "PerJobPerYear_12" AS perjobperyear_12,
    "PerWorkingYear_13" AS perworkingyear_13,
    "SexOfEmployee_label" AS sexofemployee_label,
    "TypeOfEmploymentContract_label" AS typeofemploymentcontract_label,
    "CaoSector_label" AS caosector_label,
    "JobCharacteristics_label" AS jobcharacteristics_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-81463eng"
