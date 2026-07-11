-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Sex and field of highest degree" AS sex_and_field_of_highest_degree,
    "Total" AS total,
    "Hispanic or Latino" AS hispanic_or_latino,
    "Not Hispanic or Latino - American Indian or Alaska Native" AS not_hispanic_or_latino_american_indian_or_alaska_native,
    "Not Hispanic or Latino - Asian" AS not_hispanic_or_latino_asian,
    "Not Hispanic or Latino - Black or African American" AS not_hispanic_or_latino_black_or_african_american,
    "Not Hispanic or Latino - Native Hawaiian or Other Pacific Islander" AS not_hispanic_or_latino_native_hawaiian_or_other_pacific_islander,
    "Not Hispanic or Latino - White" AS not_hispanic_or_latino_white,
    "Not Hispanic or Latino - More than one race" AS not_hispanic_or_latino_more_than_one_race,
    "Without disability - More than one race" AS without_disability_more_than_one_race,
    "With disability - More than one race" AS with_disability_more_than_one_race,
    "Type of disability - Hearing" AS type_of_disability_hearing,
    "Type of disability - Seeing" AS type_of_disability_seeing,
    "Type of disability - Walking" AS type_of_disability_walking,
    "Type of disability - Lifting" AS type_of_disability_lifting,
    "Type of disability - Cognitive" AS type_of_disability_cognitive
FROM "ncses-nsf25322-tab001-005"
