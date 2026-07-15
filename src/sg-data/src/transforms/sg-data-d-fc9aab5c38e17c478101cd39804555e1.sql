-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Average_Number_of_Training_Hours_per_Inmate_Trained" AS average_number_of_training_hours_per_inmate_trained,
    "Number_of_Inmates_Trained" AS number_of_inmates_trained
FROM "sg-data-d-fc9aab5c38e17c478101cd39804555e1"
