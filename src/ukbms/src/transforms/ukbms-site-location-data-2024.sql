-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Site_Number can appear under multiple survey types; include Survey_type when joining to site-level observations.
SELECT
    "Site_Number" AS site_number,
    "Site_Name" AS site_name,
    "Gridreference" AS gridreference,
    "Easting" AS easting,
    "Northing" AS northing,
    "Length" AS length,
    "Country" AS country,
    "N_sections" AS n_sections,
    "N_yrs_surveyed" AS n_yrs_surveyed,
    "First_year_surveyed" AS first_year_surveyed,
    "Last_year_surveyed" AS last_year_surveyed,
    "Survey_type" AS survey_type
FROM "ukbms-site-location-data-2024"
