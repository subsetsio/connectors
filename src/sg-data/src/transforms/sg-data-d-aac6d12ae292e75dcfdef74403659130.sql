-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner_Occupied" AS total_owner_occupied,
    "Total_Rented" AS total_rented,
    "Total_Others" AS total_others,
    "Single_Total" AS single_total,
    "Single_Owner_Occupied" AS single_owner_occupied,
    "Single_Rented" AS single_rented,
    "Single_Others" AS single_others,
    "Married_Total" AS married_total,
    "Married_Owner_Occupied" AS married_owner_occupied,
    "Married_Rented" AS married_rented,
    "Married_Others" AS married_others,
    "Widowed_Total" AS widowed_total,
    "Widowed_Owner_Occupied" AS widowed_owner_occupied,
    "Widowed_Rented" AS widowed_rented,
    "Widowed_Others" AS widowed_others,
    "Divorced_Separated_Total" AS divorced_separated_total,
    "Divorced_Separated_Owner_Occupied" AS divorced_separated_owner_occupied,
    "Divorced_Separated_Rented" AS divorced_separated_rented,
    "Divorced_Separated_Others" AS divorced_separated_others
FROM "sg-data-d-aac6d12ae292e75dcfdef74403659130"
