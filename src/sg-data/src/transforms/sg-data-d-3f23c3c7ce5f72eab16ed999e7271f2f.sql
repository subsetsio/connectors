-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Financial_Year" AS financial_year,
    "New_Passenger_Airlines" AS new_passenger_airlines,
    "Number_of_Airlines_with_Flights_to_Singapore" AS number_of_airlines_with_flights_to_singapore,
    "New_Passenger_City_Links" AS new_passenger_city_links,
    "Total_City_Links" AS total_city_links,
    "Passenger_Movement_in_millions" AS passenger_movement_in_millions,
    "Commercial_Aircraft_Movement" AS commercial_aircraft_movement,
    "Airfreight_Movement_in_million_tonnes" AS airfreight_movement_in_million_tonnes,
    "Registered_Aircraft" AS registered_aircraft,
    "Air_Operator_Certificate_Holders" AS air_operator_certificate_holders,
    "Certified_Aerodromes" AS certified_aerodromes,
    "Maintenance_Repair_and_Overhaul_Organisations" AS maintenance_repair_and_overhaul_organisations,
    "Design_and_Production_Organisations" AS design_and_production_organisations,
    "Aviation_Training_Organisations" AS aviation_training_organisations,
    "Maintenance_Training_Organisations" AS maintenance_training_organisations,
    "Flight_Crew_Licence_Holders" AS flight_crew_licence_holders,
    "Aircraft_Maintenance_Licence_Holders" AS aircraft_maintenance_licence_holders,
    "Air_Traffic_Controller_Licence_Holders" AS air_traffic_controller_licence_holders,
    "Total_Air_Traffic_Movement_by_FY" AS total_air_traffic_movement_by_fy,
    "Total_Emissions_from_Airport_Operations_ktCO2" AS total_emissions_from_airport_operations_ktco2,
    "Total_CO2_Emissions_from_International_Flights_MtCO2" AS total_co2_emissions_from_international_flights_mtco2,
    "UA_Registered" AS ua_registered,
    "UA_Pilot_Licence_Holders" AS ua_pilot_licence_holders,
    "Operator_Permit_Holders" AS operator_permit_holders,
    "Activity_Permits_Issued" AS activity_permits_issued,
    "UA_Basic_Training_Certificate_Holders" AS ua_basic_training_certificate_holders,
    "UA_Basic_Training_Organisations" AS ua_basic_training_organisations,
    "UA_Training_and_Assessment_Organisation" AS ua_training_and_assessment_organisation,
    "Number_of_New_Programmes" AS number_of_new_programmes,
    "Name_of_New_Programmes" AS name_of_new_programmes,
    "Number_of_Countries_where_Participants_Hail_From" AS number_of_countries_where_participants_hail_from,
    "Courses_Run" AS courses_run,
    "Total_Course_Participants_Local" AS total_course_participants_local,
    "Total_Course_Participants_International" AS total_course_participants_international,
    "Total_Course_Participants" AS total_course_participants
FROM "sg-data-d-3f23c3c7ce5f72eab16ed999e7271f2f"
