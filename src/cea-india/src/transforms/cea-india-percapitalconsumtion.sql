SELECT
    trim("Year") AS financial_year,
    TRY_CAST(split_part(trim("Year"), '-', 1) AS INTEGER) AS year_start,
    trim(state) AS state,
    TRY_CAST(value AS DOUBLE) AS per_capita_consumption_kwh
FROM "cea-india-percapitalconsumtion"
WHERE "Year" IS NOT NULL AND "Year" <> ''
