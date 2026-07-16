-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "TotalMarriageDissolutions_1" AS totalmarriagedissolutions_1,
    "MarriageDissolutionsPer1000Inhab_2" AS marriagedissolutionsper1000inhab_2,
    "MarriageDissolutionsPer1000Couples_3" AS marriagedissolutionsper1000couples_3,
    "Divorces_4" AS divorces_4,
    "DivorcesPer1000Inhabitants_5" AS divorcesper1000inhabitants_5,
    "DivorcesPer1000Couples_6" AS divorcesper1000couples_6,
    "AverageDurationOfMarriageAtDivorce_7" AS averagedurationofmarriageatdivorce_7,
    "TotalPercentageDivorces_8" AS totalpercentagedivorces_8,
    "AverageAgeOfDivorcingMen_9" AS averageageofdivorcingmen_9,
    "AverageAgeOfDivorcingWomen_10" AS averageageofdivorcingwomen_10,
    "DeceasedPartners_11" AS deceasedpartners_11,
    "DeceasedPartnersPer1000Couples_12" AS deceasedpartnersper1000couples_12,
    "DeceasedMalePartners_13" AS deceasedmalepartners_13,
    "DeceasedMalePartnersPer1000Couples_14" AS deceasedmalepartnersper1000couples_14,
    "AverageAgeOfDeceasedMalePartners_15" AS averageageofdeceasedmalepartners_15,
    "AverageAgeOfSurvivingFemalePartners_16" AS averageageofsurvivingfemalepartners_16,
    "DeceasedFemalePartners_17" AS deceasedfemalepartners_17,
    "DeceasedFemalePartnersPer1000Co_18" AS deceasedfemalepartnersper1000co_18,
    "AverageAgeOfDeceasedFemalePartners_19" AS averageageofdeceasedfemalepartners_19,
    "AverageAgeOfSurvivingMalePartners_20" AS averageageofsurvivingmalepartners_20,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-37425eng"
