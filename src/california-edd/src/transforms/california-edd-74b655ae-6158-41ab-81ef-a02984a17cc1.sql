-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual LAUS rows cover multiple local geographies; filter area type or area name before aggregating counts.
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
FROM "california-edd-74b655ae-6158-41ab-81ef-a02984a17cc1"
