-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Sex and financial resource" AS sex_and_financial_resource,
    "All fields" AS all_fields,
    "Science and engineering - Total" AS science_and_engineering_total,
    "Science and engineering - Agricultural sciences and natural resources" AS science_and_engineering_agricultural_sciences_and_natural_resources,
    "Science and engineering - Biological and biomedical sciences" AS science_and_engineering_biological_and_biomedical_sciences,
    "Science and engineering - Computer and information sciences" AS science_and_engineering_computer_and_information_sciences,
    "Science and engineering - Engineering" AS science_and_engineering_engineering,
    "Science and engineering - Geosciences atmospheric and ocean sciences" AS science_and_engineering_geosciences_atmospheric_and_ocean_sciences,
    "Science and engineering - Health sciences" AS science_and_engineering_health_sciences,
    "Science and engineering - Mathematics and statistics" AS science_and_engineering_mathematics_and_statistics,
    "Science and engineering - Multidisciplinary/ interdisciplinary sciences" AS science_and_engineering_multidisciplinary_interdisciplinary_sciences,
    "Science and engineering - Physical sciences" AS science_and_engineering_physical_sciences,
    "Science and engineering - Psychology" AS science_and_engineering_psychology,
    "Science and engineering - Social sciences" AS science_and_engineering_social_sciences,
    "Non-science and engineering - Total" AS non_science_and_engineering_total,
    "Non-science and engineering - Business" AS non_science_and_engineering_business,
    "Non-science and engineering - Education" AS non_science_and_engineering_education,
    "Non-science and engineering - Humanities" AS non_science_and_engineering_humanities,
    "Non-science and engineering - Visual and performing arts" AS non_science_and_engineering_visual_and_performing_arts,
    "Non-science and engineering - Other non-science and engineering" AS non_science_and_engineering_other_non_science_and_engineering
FROM "ncses-nsf25349-tab004-002"
