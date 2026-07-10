-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual CES rows cover statewide and substate areas; filter area type or area name before aggregating employment counts.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Name" AS area_name,
    "Area Type" AS area_type,
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    "Seasonally Adjusted(Y/N)" AS seasonally_adjusted_y_n,
    "Status" AS status,
    CAST("Labor Force" AS BIGINT) AS labor_force,
    CAST("Employment" AS BIGINT) AS employment,
    CAST("Unemployment" AS BIGINT) AS unemployment,
    CAST("Unemployment Rate" AS DOUBLE) AS unemployment_rate
FROM "california-edd-c9416284-cabe-46a3-bdbc-d00ab5ab58f7"
