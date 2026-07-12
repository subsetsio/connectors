-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Index" AS BIGINT) AS index,
    CAST("Area_unit_2013_code" AS BIGINT) AS area_unit_2013_code,
    "Area_unit_2013_label" AS area_unit_2013_label,
    CAST("Victimisations_calendar_year_2015" AS BIGINT) AS victimisations_calendar_year_2015,
    CAST("Population_mid_point_2015" AS BIGINT) AS population_mid_point_2015,
    "Rate_per_10000_population" AS rate_per_10000_population,
    "Rate_ratio_NZ_average_rate" AS rate_ratio_nz_average_rate,
    CAST("Urban_area_2013_code" AS BIGINT) AS urban_area_2013_code,
    "Urban_area_2013_label" AS urban_area_2013_label,
    "Urban_area_type" AS urban_area_type,
    CAST("Territorial_authority_area_2013_code" AS BIGINT) AS territorial_authority_area_2013_code,
    "Territorial_authority_area_2013_label" AS territorial_authority_area_2013_label,
    CAST("Region_2013_code" AS BIGINT) AS region_2013_code,
    "Region_2013_label" AS region_2013_label
FROM "statsnz-analysis-public-place-assaults-sexual-assaults-and-robberies-2015-csv"
