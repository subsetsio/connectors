-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "HighestQualificationAttainedOfHusband_NoQualification" AS highestqualificationattainedofhusband_noqualification,
    "HighestQualificationAttainedOfHusband_Primary" AS highestqualificationattainedofhusband_primary,
    "HighestQualificationAttainedOfHusband_LowerSecondary" AS highestqualificationattainedofhusband_lowersecondary,
    "HighestQualificationAttainedOfHusband_Secondary" AS highestqualificationattainedofhusband_secondary,
    "HighestQualificationAttainedOfHusband_Post_Secondary_Non_Tertia" AS highestqualificationattainedofhusband_post_secondary_non_tertia,
    "HighestQualificationAttainedOfHusband_Polytechnic" AS highestqualificationattainedofhusband_polytechnic,
    "HighestQualificationAttainedOfHusband_ProfessionalQualification" AS highestqualificationattainedofhusband_professionalqualification,
    "HighestQualificationAttainedOfHusband_University" AS highestqualificationattainedofhusband_university,
    "HighestQualificationAttainedOfHusband_Students" AS highestqualificationattainedofhusband_students
FROM "sg-data-d-299d0ae37cba6f2c357d4ce86551b9cd"
