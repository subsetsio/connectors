-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "occupation_4",
    "headcounts_full_time_equivalents_2",
    "sex_3",
    "total",
    "higher_education_sector",
    "higher_education_sector_of_which_public_universities_without_clinics",
    "higher_education_sector_of_which_university_clinics",
    "higher_education_sector_of_which_universities_of_the_arts",
    "higher_education_sector_of_which_austrian_academy_of_science",
    "higher_education_sector_of_which_fachhochschulen",
    "higher_education_sector_of_which_other",
    "higher_education_sector_of_which_private_universities",
    "higher_education_sector_of_which_universities_of_education",
    "government_sector",
    "government_sector_without_provincial_hospitals",
    "government_sector_of_which_provincial_hospitals",
    "private_non_profit_sector",
    "business_enterprise_sector",
    "business_enterprise_sector_of_which_institutes_sub_sector",
    "business_enterprise_sector_of_which_company_r_d_sub_sector"
FROM "statistics-austria-ogd-f1898-f1898-1"
