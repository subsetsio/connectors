-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Residence location" AS residence_location,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "Male - Number" AS male_number,
    "Male - SE" AS male_se,
    "Female - Number" AS female_number,
    "Female - SE" AS female_se,
    "Employment status - Employed by employment sector - All employed - Number" AS employment_status_employed_by_employment_sector_all_employed_number,
    "Employment status - Employed by employment sector - All employed - SE" AS employment_status_employed_by_employment_sector_all_employed_se,
    "Employment status - Employed by employment sector - Educational institution - Number" AS employment_status_employed_by_employment_sector_educational_institution_number,
    "Employment status - Employed by employment sector - Educational institution - SE" AS employment_status_employed_by_employment_sector_educational_institution_se,
    "Employment status - Employed by employment sector - Business or industry - Number" AS employment_status_employed_by_employment_sector_business_or_industry_number,
    "Employment status - Employed by employment sector - Business or industry - SE" AS employment_status_employed_by_employment_sector_business_or_industry_se,
    "Employment status - Employed by employment sector - Government - Number" AS employment_status_employed_by_employment_sector_government_number,
    "Employment status - Employed by employment sector - Government - SE" AS employment_status_employed_by_employment_sector_government_se,
    "Employment status - Unemployeda - Government - Number" AS employment_status_unemployeda_government_number,
    "Employment status - Unemployeda - Government - SE" AS employment_status_unemployeda_government_se,
    "Employment status - Not in the labor forceb - Government - Number" AS employment_status_not_in_the_labor_forceb_government_number,
    "Employment status - Not in the labor forceb - Government - SE" AS employment_status_not_in_the_labor_forceb_government_se
FROM "ncses-nsf25321-tab078"
