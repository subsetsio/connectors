-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "BelowSecondary_Total" AS belowsecondary_total,
    "BelowSecondary_Males" AS belowsecondary_males,
    "BelowSecondary_Females" AS belowsecondary_females,
    "Secondary_Total" AS secondary_total,
    "Secondary_Males" AS secondary_males,
    "Secondary_Females" AS secondary_females,
    "Post_Secondary_Total" AS post_secondary_total,
    "Post_Secondary_Males" AS post_secondary_males,
    "Post_Secondary_Females" AS post_secondary_females,
    "University_Total" AS university_total,
    "University_Males" AS university_males,
    "University_Females" AS university_females
FROM "sg-data-d-b689ed11b559ec47ead45c4a91c63cf7"
