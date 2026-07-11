-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "All R and D expenditures" AS all_r_and_d_expenditures,
    "Computer and information sciences" AS computer_and_information_sciences,
    "Geosciences atmospheric sciences and ocean sciences" AS geosciences_atmospheric_sciences_and_ocean_sciences,
    "Life sciences" AS life_sciences,
    "Mathematics and statistics" AS mathematics_and_statistics,
    "Physical sciences" AS physical_sciences,
    "Psychology" AS psychology,
    "Social sciences" AS social_sciences,
    "Sciences nec" AS sciences_nec,
    "Engineering" AS engineering,
    "All non-S and E fields" AS all_non_s_and_e_fields
FROM "ncses-nsf26304-tab017"
