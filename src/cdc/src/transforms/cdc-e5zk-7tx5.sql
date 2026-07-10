-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Season" AS season,
    "Month" AS month,
    CAST("Month_Number" AS BIGINT) AS month_number,
    CAST("Week" AS BIGINT) AS week,
    "Month_Week_Label" AS month_week_label,
    CAST("Month_Week_Sort_Order" AS BIGINT) AS month_week_sort_order,
    CAST("Cumulative_Flu_Doses_Distributed" AS DOUBLE) AS cumulative_flu_doses_distributed,
    CAST("Imputed_Value" AS BOOLEAN) AS imputed_value,
    "Current_Through" AS current_through
FROM "cdc-e5zk-7tx5"
