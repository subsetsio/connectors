-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Below65Years" AS total_below65years,
    "Total_65YearsandOver" AS total_65yearsandover,
    "BelowSecondary_Total" AS belowsecondary_total,
    "BelowSecondary_Below65Years" AS belowsecondary_below65years,
    "BelowSecondary_65YearsandOver" AS belowsecondary_65yearsandover,
    "Secondary_Total" AS secondary_total,
    "Secondary_Below65Years" AS secondary_below65years,
    "Secondary_65YearsandOver" AS secondary_65yearsandover,
    "Post_Secondary_Non_Tertiary_Total" AS post_secondary_non_tertiary_total,
    "Post_Secondary_Non_Tertiary_Below65Years" AS post_secondary_non_tertiary_below65years,
    "Post_Secondary_Non_Tertiary_65YearsandOver" AS post_secondary_non_tertiary_65yearsandover,
    "Diploma2_andProfessionalQualification_Total" AS diploma2_andprofessionalqualification_total,
    "Diploma2_andProfessionalQualification_Below65Years" AS diploma2_andprofessionalqualification_below65years,
    "Diploma2_andProfessionalQualification_65YearsandOver" AS diploma2_andprofessionalqualification_65yearsandover,
    "University_Total" AS university_total,
    "University_Below65Years" AS university_below65years,
    "University_65YearsandOver" AS university_65yearsandover
FROM "sg-data-d-aed3494f1f6f32d240f7965347363c0c"
