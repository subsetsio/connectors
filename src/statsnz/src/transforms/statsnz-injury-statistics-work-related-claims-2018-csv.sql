-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Year" AS BIGINT) AS year,
    "Sex" AS sex,
    "Age group (years) at date of injury" AS age_group_years_at_date_of_injury,
    "Geographic region where injury occurred" AS geographic_region_where_injury_occurred,
    "Employment status" AS employment_status,
    "Occupation" AS occupation,
    "Injury/illness/disease group" AS injury_illness_disease_group,
    "Type of injury/illness/disease" AS type_of_injury_illness_disease,
    "Industry" AS industry,
    "Industry subgroup" AS industry_subgroup,
    CAST("Value" AS DOUBLE) AS value,
    "Measure" AS measure,
    "Status" AS status
FROM "statsnz-injury-statistics-work-related-claims-2018-csv"
