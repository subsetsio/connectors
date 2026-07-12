-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Direction" AS direction,
    CAST("Year" AS BIGINT) AS year,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Weekday" AS weekday,
    "Country" AS country,
    "Commodity" AS commodity,
    "Transport_Mode" AS transport_mode,
    "Measure" AS measure,
    CAST("Value" AS BIGINT) AS value,
    CAST("Cumulative" AS BIGINT) AS cumulative
FROM "statsnz-effects-of-covid-19-on-trade-at-15-december-2021-provisional"
