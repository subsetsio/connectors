-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Employment commitment sector and year - All U.S. employment commitments number" AS employment_commitment_sector_and_year_all_u_s_employment_commitments_number,
    "All fields - All U.S. employment commitments number" AS all_fields_all_u_s_employment_commitments_number,
    "Science and engineering - Total - All U.S. employment commitments number" AS science_and_engineering_total_all_u_s_employment_commitments_number,
    "Science and engineering - Agricultural sciences and natural resources - All U.S. employment commitments number" AS science_and_engineering_agricultural_sciences_and_natural_resources_all_u_s_employment_commitments_number,
    "Science and engineering - Biological and biomedical sciences - All U.S. employment commitments number" AS science_and_engineering_biological_and_biomedical_sciences_all_u_s_employment_commitments_number,
    "Science and engineering - Computer and information sciences - All U.S. employment commitments number" AS science_and_engineering_computer_and_information_sciences_all_u_s_employment_commitments_number,
    "Science and engineering - Engineering - All U.S. employment commitments number" AS science_and_engineering_engineering_all_u_s_employment_commitments_number,
    "Science and engineering - Geosciences atmospheric and ocean sciences - All U.S. employment commitments number" AS science_and_engineering_geosciences_atmospheric_and_ocean_sciences_all_u_s_employment_commitments_number,
    "Science and engineering - Health sciences - All U.S. employment commitments number" AS science_and_engineering_health_sciences_all_u_s_employment_commitments_number,
    "Science and engineering - Mathematics and statistics - All U.S. employment commitments number" AS science_and_engineering_mathematics_and_statistics_all_u_s_employment_commitments_number,
    "Science and engineering - Physical sciences - All U.S. employment commitments number" AS science_and_engineering_physical_sciences_all_u_s_employment_commitments_number,
    "Science and engineering - Psychology - All U.S. employment commitments number" AS science_and_engineering_psychology_all_u_s_employment_commitments_number,
    "Science and engineering - Social sciences - All U.S. employment commitments number" AS science_and_engineering_social_sciences_all_u_s_employment_commitments_number,
    "Non-science and engineering - Total - All U.S. employment commitments number" AS non_science_and_engineering_total_all_u_s_employment_commitments_number,
    "Non-science and engineering - Business - All U.S. employment commitments number" AS non_science_and_engineering_business_all_u_s_employment_commitments_number,
    "Non-science and engineering - Education - All U.S. employment commitments number" AS non_science_and_engineering_education_all_u_s_employment_commitments_number,
    "Non-science and engineering - Humanities and arts - All U.S. employment commitments number" AS non_science_and_engineering_humanities_and_arts_all_u_s_employment_commitments_number,
    "Non-science and engineering - Other non-science and engineering - All U.S. employment commitments number" AS non_science_and_engineering_other_non_science_and_engineering_all_u_s_employment_commitments_number
FROM "ncses-nsf25349-tab002-006"
