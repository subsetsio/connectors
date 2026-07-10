-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pathogen" AS pathogen,
    "table_id",
    "Food_category" AS food_category,
    CAST("Year" AS BIGINT) AS year,
    "Serotype" AS serotype,
    "Burden" AS burden,
    "Trajectory" AS trajectory,
    "Year_range" AS year_range,
    CAST("No_of_illnesses" AS BIGINT) AS no_of_illnesses,
    CAST("Hospitalization(s)" AS BIGINT) AS hospitalization_s,
    CAST("Burden_sort_order" AS BIGINT) AS burden_sort_order,
    CAST("Trajectory_sort_order" AS BIGINT) AS trajectory_sort_order,
    CAST("Master_sort_order" AS BIGINT) AS master_sort_order
FROM "cdc-8na9-qgz7"
