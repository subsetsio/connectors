-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of study" AS field_of_study,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "Computer applications - Median salary" AS computer_applications_median_salary,
    "Computer applications - SE" AS computer_applications_se,
    "Design - Median salary" AS design_median_salary,
    "Design - SE" AS design_se,
    "Management sales or administrationa - Median salary" AS management_sales_or_administrationa_median_salary,
    "Management sales or administrationa - SE" AS management_sales_or_administrationa_se,
    "Professional services - Median salary" AS professional_services_median_salary,
    "Professional services - SE" AS professional_services_se,
    "Any R and Db - Median salary" AS any_r_and_db_median_salary,
    "Any R and Db - SE" AS any_r_and_db_se,
    "Teaching - Median salary" AS teaching_median_salary,
    "Teaching - SE" AS teaching_se,
    "Otherc - Median salary" AS otherc_median_salary,
    "Otherc - SE" AS otherc_se
FROM "ncses-nsf25321-tab057-002"
