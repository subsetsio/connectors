-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Level of highest degree and occupation" AS level_of_highest_degree_and_occupation,
    "Total" AS total,
    "Obtained a certification or license for work-related reasons" AS obtained_a_certification_or_license_for_work_related_reasons,
    "Primary field of certification or license - Computer applications and design" AS primary_field_of_certification_or_license_computer_applications_and_design,
    "Primary field of certification or license - Computer networking administration and security" AS primary_field_of_certification_or_license_computer_networking_administration_and_security,
    "Primary field of certification or license - Other information technologies and computers" AS primary_field_of_certification_or_license_other_information_technologies_and_computers,
    "Primary field of certification or license - Mathematics statistics and data analytics" AS primary_field_of_certification_or_license_mathematics_statistics_and_data_analytics,
    "Primary field of certification or license - Life sciences" AS primary_field_of_certification_or_license_life_sciences,
    "Primary field of certification or license - Physical sciences" AS primary_field_of_certification_or_license_physical_sciences,
    "Primary field of certification or license - Social sciences" AS primary_field_of_certification_or_license_social_sciences,
    "Primary field of certification or license - Engineering" AS primary_field_of_certification_or_license_engineering,
    "Primary field of certification or license - S and E-related" AS primary_field_of_certification_or_license_s_and_e_related,
    "Primary field of certification or license - Non-S and E" AS primary_field_of_certification_or_license_non_s_and_e,
    "Primary field of certification or license - Uncodeable or missing" AS primary_field_of_certification_or_license_uncodeable_or_missing
FROM "ncses-nsf25322-tab002-006"
