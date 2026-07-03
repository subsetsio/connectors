-- Statistical Review of World Energy — tidy long form.
-- The raw is the source's wide "panel" CSV: one row per country/region-year with
-- ~90 energy-measure columns. UNPIVOT folds every measure column into a
-- (measure_code, value) pair so the published table is a clean EAV long table:
-- one row per country-year-measure. The dimension/identity columns (Country,
-- Year, the ISO codes, Region/SubRegion, and the OPEC/EU/OECD/CIS membership
-- flags) are EXCLUDEd from the unpivot and kept as row attributes; `pop`
-- (population) is deliberately left in the measure set as measure_code='pop'.
WITH long AS (
    UNPIVOT "energy-institute-values"
    ON COLUMNS(* EXCLUDE (
        Country, Year, ISO3166_alpha3, ISO3166_numeric,
        Region, SubRegion, OPEC, EU, OECD, CIS
    ))
    INTO NAME measure_code VALUE value
)
SELECT
    Country                AS country,
    CAST(Year AS INTEGER)  AS year,
    ISO3166_alpha3         AS iso3,
    Region                 AS region,
    SubRegion              AS subregion,
    measure_code,
    CAST(value AS DOUBLE)  AS value
FROM long
WHERE value IS NOT NULL
