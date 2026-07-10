-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dhds_test_row_3",
    CAST("2021" AS BIGINT) AS 2021,
    "HHS6" AS hhs6,
    "HHS Region 6" AS hhs_region_6,
    "BRFSS" AS brfss,
    "Disability Estimates" AS disability_estimates,
    "Disability status and types among adults 18 years of age or older" AS disability_status_and_types_among_adults_18_years_of_age_or_older,
    "Any Disability" AS any_disability,
    "%" AS column,
    "Age-adjusted Prevalence" AS age_adjusted_prevalence,
    CAST("29.4" AS DOUBLE) AS 29_4,
    CAST("29.4_1" AS DOUBLE) AS 29_4_1,
    "column12",
    "column13",
    CAST("28.3" AS DOUBLE) AS 28_3,
    CAST("30.5" AS DOUBLE) AS 30_5,
    CAST("11208" AS BIGINT) AS 11208,
    CAST("9290557" AS BIGINT) AS 9290557,
    "Overall" AS overall,
    "Overall_1" AS overall_1,
    "column20",
    "column21",
    "DISEST" AS disest,
    "STATTYPE" AS stattype,
    "column24",
    "05",
    "Q6DIS1" AS q6dis1,
    "AGEADJPREV" AS ageadjprev,
    "CAT1" AS cat1,
    "BO1" AS bo1
FROM "cdc-bx8m-di6q"
