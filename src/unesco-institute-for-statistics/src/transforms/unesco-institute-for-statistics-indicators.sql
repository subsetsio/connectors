-- caution: `last_data_update` is the indicator's upstream revision date, not an observation period — it says nothing about which years the indicator covers.
-- caution: The catalog lists every indicator UIS defines, including ones with no observations in the values table.
-- lastDataUpdate arrives as m/d/Y: the only value observed, 02/09/2026, would fall
-- in the future read as d/m/Y, which a "last updated" date cannot be.
-- geo_unit_types arrives as a comma string whose member order is not stable
-- (both NATIONAL,REGIONAL and REGIONAL,NATIONAL occur) — sorted here so equal sets compare equal.
SELECT
    "indicator_code",
    "name",
    "theme",
    CAST(strptime("last_data_update", '%m/%d/%Y') AS DATE)                      AS last_data_update,
    "last_data_update_description",
    "total_record_count",
    "year_min",
    "year_max",
    array_to_string(list_sort(string_split("geo_unit_types", ',')), ',')        AS geo_unit_types
FROM "unesco-institute-for-statistics-indicators"
