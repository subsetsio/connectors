-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "_5_digit_ntd_id" AS 5_digit_ntd_id,
    "agency",
    "uace_code",
    "rail_bus_fetty",
    "mode_name",
    "mode",
    "type_of_service",
    CAST("fixed_route_flag" AS BOOLEAN) AS fixed_route_flag,
    CAST("rail_y_n" AS BOOLEAN) AS rail_y_n,
    "month",
    CAST("year" AS BIGINT) AS year,
    "sftsecfl",
    "eventtype",
    "location",
    "location_group",
    CAST("minor_physical_assaults_on_operators" AS BIGINT) AS minor_physical_assaults_on_operators,
    CAST("non_physical_assaults_on_operators_security_events_only_" AS BIGINT) AS non_physical_assaults_on_operators_security_events_only,
    CAST("minor_physical_assaults_on_other_transit_workers" AS BIGINT) AS minor_physical_assaults_on_other_transit_workers,
    CAST("minor_nonphysical_assaults_on_other_transit_workers" AS BIGINT) AS minor_nonphysical_assaults_on_other_transit_workers,
    "additional_assault_information",
    CAST("total_incidents" AS BIGINT) AS total_incidents,
    CAST("customer" AS BIGINT) AS customer,
    CAST("worker" AS BIGINT) AS worker,
    CAST("other" AS BIGINT) AS other,
    CAST("total_injuries" AS BIGINT) AS total_injuries
FROM "u-s-department-of-transportation-urir-txqm"
