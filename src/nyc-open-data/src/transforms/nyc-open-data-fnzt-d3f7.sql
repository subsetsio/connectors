-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school",
    "leadership",
    "teachers",
    "other_staff",
    "male_count",
    "male_average_years_in_title",
    "male_average_years_at_school",
    "female_count",
    "female_average_years_in_title",
    "female_average_years_at_school",
    "male_count_1",
    "male_average_years_in_title_1",
    "male_average_years_at_school_1",
    "female_count_1",
    "female_average_years_in_title_1",
    "female_average_years_at_school_1",
    "male_count_2",
    "male_average_years_in_title_2",
    "male_average_years_at_school_2",
    "female_count_2",
    "female_average_years_in_title_2",
    "female_average_years_at_school_2"
FROM "nyc-open-data-fnzt-d3f7"
