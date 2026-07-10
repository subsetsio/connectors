-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("ID" AS BIGINT) AS id,
    CAST("SiteID" AS BIGINT) AS siteid,
    CAST("Year" AS BIGINT) AS year,
    "Contributing Factor" AS contributing_factor,
    CAST("Lack of training of employees on specific processes" AS BIGINT) AS lack_of_training_of_employees_on_specific_processes,
    CAST("Lack of oversight of employees/ enforcement of policies" AS BIGINT) AS lack_of_oversight_of_employees_enforcement_of_policies,
    CAST("High turnover of employees or management" AS BIGINT) AS high_turnover_of_employees_or_management,
    CAST("Low/insufficient staffing" AS BIGINT) AS low_insufficient_staffing,
    CAST("Lack of a food safety culture/ attitude towards food safety" AS BIGINT) AS lack_of_a_food_safety_culture_attitude_towards_food_safety,
    CAST("Language barrier between management and employees" AS BIGINT) AS language_barrier_between_management_and_employees,
    CAST("Insufficient capacity of equipment (not  
   enough equipment for the processes)" AS BIGINT) AS insufficient_capacity_of_equipment_not_enough_equipment_for_the_processes,
    CAST("Equipment is improperly used" AS BIGINT) AS equipment_is_improperly_used,
    CAST("Lack of preventative maintenance on equipment" AS BIGINT) AS lack_of_preventative_maintenance_on_equipment,
    CAST("Improperly sized or installed equipment for the facility" AS BIGINT) AS improperly_sized_or_installed_equipment_for_the_facility,
    CAST("Poor facility layout" AS BIGINT) AS poor_facility_layout,
    CAST("Lack of reinvestment in the restaurant" AS BIGINT) AS lack_of_reinvestment_in_the_restaurant,
    CAST("Lack of sick leave or other financial incentives to adhere to good practices" AS BIGINT) AS lack_of_sick_leave_or_other_financial_incentives_to_adhere_to_good_practices,
    CAST("Lack of needed supplies for the operation of the restaurant" AS BIGINT) AS lack_of_needed_supplies_for_the_operation_of_the_restaurant,
    CAST("Insufficient process to mitigate the hazard" AS BIGINT) AS insufficient_process_to_mitigate_the_hazard,
    CAST("Employees or managers are not following the
  facility’s process" AS BIGINT) AS employees_or_managers_are_not_following_the_facility_s_process,
    CAST("Food not treated as time and temperature
 control for safety" AS BIGINT) AS food_not_treated_as_time_and_temperature_control_for_safety,
    CAST("Other" AS BIGINT) AS other
FROM "cdc-4khb-4xch"
