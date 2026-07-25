-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("data_year" AS BIGINT) AS data_year,
    CAST("state_fips_code" AS BIGINT) AS state_fips_code,
    CAST("county_fips_code" AS BIGINT) AS county_fips_code,
    CAST("rural_urban" AS BIGINT) AS rural_urban,
    CAST("urbanized_sampling_technique" AS BIGINT) AS urbanized_sampling_technique,
    CAST("urbanized_area_code" AS BIGINT) AS urbanized_area_code,
    CAST("type_of_section" AS BIGINT) AS type_of_section,
    "section_identification",
    CAST("functional_class" AS BIGINT) AS functional_class,
    CAST("federal_aid_system" AS BIGINT) AS federal_aid_system,
    CAST("route_signing" AS BIGINT) AS route_signing,
    CAST("federal_aid_system_status" AS BIGINT) AS federal_aid_system_status,
    CAST("route_signing_1" AS BIGINT) AS route_signing_1,
    "route_number",
    CAST("governmental_level_of_control" AS BIGINT) AS governmental_level_of_control,
    CAST("federal_state_and_local_domain" AS BIGINT) AS federal_state_and_local_domain,
    CAST("special_systems" AS BIGINT) AS special_systems,
    CAST("type_of_facility" AS BIGINT) AS type_of_facility,
    CAST("toll" AS BIGINT) AS toll,
    CAST("section_grouped_length" AS DOUBLE) AS section_grouped_length,
    CAST("aadt" AS BIGINT) AS aadt,
    CAST("number_of_through_lanes" AS BIGINT) AS number_of_through_lanes
FROM "u-s-department-of-transportation-mhuc-n78n"
