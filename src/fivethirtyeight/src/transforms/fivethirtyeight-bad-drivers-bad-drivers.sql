-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "Number of drivers involved in fatal collisions per billion miles" AS number_of_drivers_involved_in_fatal_collisions_per_billion_miles,
    "Percentage Of Drivers Involved In Fatal Collisions Who Were Speeding" AS percentage_of_drivers_involved_in_fatal_collisions_who_were_speeding,
    "Percentage Of Drivers Involved In Fatal Collisions Who Were Alcohol-Impaired" AS percentage_of_drivers_involved_in_fatal_collisions_who_were_alcohol_impaired,
    "Percentage Of Drivers Involved In Fatal Collisions Who Were Not Distracted" AS percentage_of_drivers_involved_in_fatal_collisions_who_were_not_distracted,
    "Percentage Of Drivers Involved In Fatal Collisions Who Had Not Been Involved In Any Previous Accidents" AS percentage_of_drivers_involved_in_fatal_collisions_who_had_not_been_involved_in_any_previous_accidents,
    "Car Insurance Premiums ($)" AS car_insurance_premiums,
    "Losses incurred by insurance companies for collisions per insured driver ($)" AS losses_incurred_by_insurance_companies_for_collisions_per_insured_driver
FROM "fivethirtyeight-bad-drivers-bad-drivers"
