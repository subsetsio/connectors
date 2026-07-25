-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("date_year" AS BIGINT) AS date_year,
    CAST("state_fips_code" AS BIGINT) AS state_fips_code,
    CAST("rural_urban" AS BIGINT) AS rural_urban,
    CAST("urbanized_sampling_technique" AS BIGINT) AS urbanized_sampling_technique,
    CAST("urbanized_area_code" AS BIGINT) AS urbanized_area_code,
    CAST("federal_aid_system" AS BIGINT) AS federal_aid_system,
    CAST("federal_aid_system_status" AS BIGINT) AS federal_aid_system_status,
    "route_signing",
    CAST("route_number" AS BIGINT) AS route_number,
    CAST("governmental_level_of_control" AS BIGINT) AS governmental_level_of_control,
    CAST("special_systems" AS BIGINT) AS special_systems,
    CAST("type_of_facility" AS BIGINT) AS type_of_facility,
    CAST("designated_truck_route_parkway" AS BIGINT) AS designated_truck_route_parkway,
    "toll",
    CAST("section_grouped_length" AS BIGINT) AS section_grouped_length,
    CAST("aadt" AS BIGINT) AS aadt,
    CAST("number_of_through_lanes" AS BIGINT) AS number_of_through_lanes,
    CAST("unnamed_column" AS BIGINT) AS unnamed_column,
    CAST("unnamed_column_1" AS BIGINT) AS unnamed_column_1,
    CAST("unnamed_column_2" AS DOUBLE) AS unnamed_column_2,
    CAST("unnamed_column_3" AS BIGINT) AS unnamed_column_3,
    CAST("unnamed_column_4" AS BIGINT) AS unnamed_column_4
FROM "u-s-department-of-transportation-dbr2-hxmv"
