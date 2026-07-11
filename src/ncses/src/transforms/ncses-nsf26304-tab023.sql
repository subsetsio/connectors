-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "2022",
    "2023",
    "2024 - All non-S and E fields" AS "2024_all_non_s_and_e_fields",
    "2024 - Business management and business administration" AS "2024_business_management_and_business_administration",
    "2024 - Communication and communications technologies" AS "2024_communication_and_communications_technologies",
    "2024 - Education" AS "2024_education",
    "2024 - Humanities" AS "2024_humanities",
    "2024 - Law" AS "2024_law",
    "2024 - Social work" AS "2024_social_work",
    "2024 - Visual and performing arts" AS "2024_visual_and_performing_arts",
    "2024 - Non-S and E nec" AS "2024_non_s_and_e_nec"
FROM "ncses-nsf26304-tab023"
