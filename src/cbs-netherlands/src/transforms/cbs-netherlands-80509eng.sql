-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "TotalGovernmentExpenditure_1" AS totalgovernmentexpenditure_1,
    "TotalGovernmentExpOnEducation_2" AS totalgovernmentexponeducation_2,
    "TotalPrePrimaryEducation_3" AS totalpreprimaryeducation_3,
    "PrePrimaryAndPrimaryEducation_4" AS preprimaryandprimaryeducation_4,
    "SpecialNeedsPrimaryEducation_5" AS specialneedsprimaryeducation_5,
    "TotalSecondaryEducation_6" AS totalsecondaryeducation_6,
    "SecondaryGeneralEducation_7" AS secondarygeneraleducation_7,
    "SeniorVocAndGenAdultSecEduc_8" AS seniorvocandgenadultseceduc_8,
    "TotalTertiaryEducation_9" AS totaltertiaryeducation_9,
    "HigherProfessionalEducation_10" AS higherprofessionaleducation_10,
    "UniversityEducation_11" AS universityeducation_11,
    "TotalStudentGrantsLoansAndAllow_12" AS totalstudentgrantsloansandallow_12,
    "TotalSecondaryEducation_13" AS totalsecondaryeducation_13,
    "SecondaryGeneralEducation_14" AS secondarygeneraleducation_14,
    "SeniorVocAndGenAdultSecEduc_15" AS seniorvocandgenadultseceduc_15,
    "TotalTertiaryEducation_16" AS totaltertiaryeducation_16,
    "HigherProfessionalEducation_17" AS higherprofessionaleducation_17,
    "UniversityEducation_18" AS universityeducation_18,
    "TotalGovernmentExpenditureAsOfGDP_19" AS totalgovernmentexpenditureasofgdp_19,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80509eng"
