-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Occupation" AS occupation,
    "Total" AS total,
    "S and E fields - Total" AS s_and_e_fields_total,
    "S and E fields - Biological agricultural and environmental life sciences" AS s_and_e_fields_biological_agricultural_and_environmental_life_sciences,
    "S and E fields - Computer and mathematical sciences" AS s_and_e_fields_computer_and_mathematical_sciences,
    "S and E fields - Physical and related sciences" AS s_and_e_fields_physical_and_related_sciences,
    "S and E fields - Social and related sciences" AS s_and_e_fields_social_and_related_sciences,
    "S and E fields - Engineering" AS s_and_e_fields_engineering,
    "S and E-related fields - Engineering" AS s_and_e_related_fields_engineering,
    "Non-S and E fields - Engineering" AS non_s_and_e_fields_engineering
FROM "ncses-nsf25322-tab002-004"
