-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Year" AS year,
    CAST("Month" AS BIGINT) AS month,
    "Group" AS group,
    "State" AS state,
    "Indicator" AS indicator,
    CAST("Non-Hispanic White" AS DOUBLE) AS non_hispanic_white,
    CAST("Non-Hispanic Black or African American" AS DOUBLE) AS non_hispanic_black_or_african_american,
    CAST("Non-Hispanic American Indian or Alaska Native" AS DOUBLE) AS non_hispanic_american_indian_or_alaska_native,
    CAST("Non-Hispanic Asian" AS DOUBLE) AS non_hispanic_asian,
    CAST("Non-Hispanic Native Hawaiian or Other Pacific Islander" AS DOUBLE) AS non_hispanic_native_hawaiian_or_other_pacific_islander,
    CAST("Non Hispanic more than one race" AS DOUBLE) AS non_hispanic_more_than_one_race,
    CAST("Hispanic or Latino" AS DOUBLE) AS hispanic_or_latino,
    "Footnote" AS footnote
FROM "cdc-pj7m-y5uh"
