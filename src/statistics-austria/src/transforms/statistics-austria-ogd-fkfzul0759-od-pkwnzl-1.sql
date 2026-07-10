-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "passenger_car_makes",
    "time_monthly_values",
    "fahrzeug",
    "number_of_registrations_of_new_vehicles"
FROM "statistics-austria-ogd-fkfzul0759-od-pkwnzl-1"
