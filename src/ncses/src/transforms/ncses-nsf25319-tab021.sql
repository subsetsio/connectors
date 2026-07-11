-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State or territory control and institution" AS state_or_territory_control_and_institution,
    "All fields" AS all_fields,
    "Agricultural sciences" AS agricultural_sciences,
    "Biological and biomedical sciences" AS biological_and_biomedical_sciences,
    "Computer and information sciences" AS computer_and_information_sciences,
    "Engineering" AS engineering,
    "Geosciences atmospheric sciences and ocean sciences" AS geosciences_atmospheric_sciences_and_ocean_sciences,
    "Health sciences" AS health_sciences,
    "Mathematics and statistics" AS mathematics_and_statistics,
    "Natural resources and conservation" AS natural_resources_and_conservation,
    "Physical sciences" AS physical_sciences,
    "Psychology" AS psychology,
    "Social sciences" AS social_sciences,
    "Other fields of S and E" AS other_fields_of_s_and_e
FROM "ncses-nsf25319-tab021"
