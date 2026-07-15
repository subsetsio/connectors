-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_AgeGroup_Years_Below25" AS total_agegroup_years_below25,
    "Total_AgeGroup_Years_25_29" AS total_agegroup_years_25_29,
    "Total_AgeGroup_Years_30_34" AS total_agegroup_years_30_34,
    "Total_AgeGroup_Years_35_39" AS total_agegroup_years_35_39,
    "Total_AgeGroup_Years_40_44" AS total_agegroup_years_40_44,
    "Total_AgeGroup_Years_45_49" AS total_agegroup_years_45_49,
    "Total_AgeGroup_Years_50_54" AS total_agegroup_years_50_54,
    "Total_AgeGroup_Years_55_59" AS total_agegroup_years_55_59,
    "Total_AgeGroup_Years_60_64" AS total_agegroup_years_60_64,
    "Total_AgeGroup_Years_65andOver" AS total_agegroup_years_65andover,
    "Males_Total" AS males_total,
    "Males_AgeGroup_Years_Below25" AS males_agegroup_years_below25,
    "Males_AgeGroup_Years_25_29" AS males_agegroup_years_25_29,
    "Males_AgeGroup_Years_30_34" AS males_agegroup_years_30_34,
    "Males_AgeGroup_Years_35_39" AS males_agegroup_years_35_39,
    "Males_AgeGroup_Years_40_44" AS males_agegroup_years_40_44,
    "Males_AgeGroup_Years_45_49" AS males_agegroup_years_45_49,
    "Males_AgeGroup_Years_50_54" AS males_agegroup_years_50_54,
    "Males_AgeGroup_Years_55_59" AS males_agegroup_years_55_59,
    "Males_AgeGroup_Years_60_64" AS males_agegroup_years_60_64,
    "Males_AgeGroup_Years_65andOver" AS males_agegroup_years_65andover,
    "Females_Total" AS females_total,
    "Females_AgeGroup_Years_Below25" AS females_agegroup_years_below25,
    "Females_AgeGroup_Years_25_29" AS females_agegroup_years_25_29,
    "Females_AgeGroup_Years_30_34" AS females_agegroup_years_30_34,
    "Females_AgeGroup_Years_35_39" AS females_agegroup_years_35_39,
    "Females_AgeGroup_Years_40_44" AS females_agegroup_years_40_44,
    "Females_AgeGroup_Years_45_49" AS females_agegroup_years_45_49,
    "Females_AgeGroup_Years_50_54" AS females_agegroup_years_50_54,
    "Females_AgeGroup_Years_55_59" AS females_agegroup_years_55_59,
    "Females_AgeGroup_Years_60_64" AS females_agegroup_years_60_64,
    "Females_AgeGroup_Years_65andOver" AS females_agegroup_years_65andover
FROM "sg-data-d-32befe3f2df372112752286864cd3b61"
