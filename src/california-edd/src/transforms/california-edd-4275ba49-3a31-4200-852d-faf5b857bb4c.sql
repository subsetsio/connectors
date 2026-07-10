-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include both California and United States unemployment-rate observations, with separate seasonally adjusted and not-seasonally adjusted rate columns.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Date" AS date,
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    CAST("Seasonally Adjusted" AS DOUBLE) AS seasonally_adjusted,
    CAST("Not Seasonally Adjusted" AS DOUBLE) AS not_seasonally_adjusted
FROM "california-edd-4275ba49-3a31-4200-852d-faf5b857bb4c"
