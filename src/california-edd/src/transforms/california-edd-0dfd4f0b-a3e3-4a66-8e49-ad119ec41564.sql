-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly unemployment insurance rows include both filed-week and reflecting-week dates; use the appropriate week for the measure being analyzed.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    strptime("Filed week ended", '%m/%d/%Y')::DATE AS filed_week_ended,
    CAST("Initial Claims" AS BIGINT) AS initial_claims,
    strptime("Reflecting Week Ended", '%m/%d/%Y')::DATE AS reflecting_week_ended,
    CAST("Continued Claims" AS BIGINT) AS continued_claims,
    CAST("Covered Employment" AS BIGINT) AS covered_employment,
    CAST("Insured Unemployment Rate" AS DOUBLE) AS insured_unemployment_rate
FROM "california-edd-0dfd4f0b-a3e3-4a66-8e49-ad119ec41564"
