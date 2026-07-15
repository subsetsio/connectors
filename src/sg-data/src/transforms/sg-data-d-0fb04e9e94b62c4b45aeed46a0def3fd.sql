-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "AgeGroup_Years_0_4" AS agegroup_years_0_4,
    "AgeGroup_Years_5_9" AS agegroup_years_5_9,
    "AgeGroup_Years_10_14" AS agegroup_years_10_14,
    "AgeGroup_Years_15_19" AS agegroup_years_15_19,
    "AgeGroup_Years_20_24" AS agegroup_years_20_24,
    "AgeGroup_Years_25_29" AS agegroup_years_25_29,
    "AgeGroup_Years_30_34" AS agegroup_years_30_34,
    "AgeGroup_Years_35_39" AS agegroup_years_35_39,
    "AgeGroup_Years_40_44" AS agegroup_years_40_44,
    "AgeGroup_Years_45_49" AS agegroup_years_45_49,
    "AgeGroup_Years_50_54" AS agegroup_years_50_54,
    "AgeGroup_Years_55_59" AS agegroup_years_55_59,
    "AgeGroup_Years_60_64" AS agegroup_years_60_64,
    "AgeGroup_Years_65andOver" AS agegroup_years_65andover
FROM "sg-data-d-0fb04e9e94b62c4b45aeed46a0def3fd"
