-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "row_number",
    "OBJECTID" AS objectid,
    "School identification number" AS school_identification_number,
    "Name of institution" AS name_of_institution,
    "Reported street address" AS reported_street_address,
    "Reported city" AS reported_city,
    "Reported state" AS reported_state,
    "Reported ZIP code" AS reported_zip_code,
    "State FIPS" AS state_fips,
    "County FIPS" AS county_fips,
    "County name" AS county_name,
    "Locale code" AS locale_code,
    "Latitude of school location" AS latitude_of_school_location,
    "Longitude of school location" AS longitude_of_school_location,
    "Core Based Statistical Area" AS core_based_statistical_area,
    "Core Based Statistical Area name" AS core_based_statistical_area_name,
    "Metropolitan or Micropolitan Statistical Area indicator" AS metropolitan_or_micropolitan_statistical_area_indicator,
    "Combined Statistical Area" AS combined_statistical_area,
    "Combined Statistical Area name" AS combined_statistical_area_name,
    "Congressional District" AS congressional_district,
    "State Legislative District - Lower" AS state_legislative_district_lower,
    "State Legislative District - Upper" AS state_legislative_district_upper,
    "School Year" AS school_year,
    "x",
    "y",
    "_subsets_record_type" AS subsets_record_type,
    "error"
FROM "u-s-department-of-education-postsecondary-school-locations-current"
