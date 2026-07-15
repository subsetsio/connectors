-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "distance",
    "cash_fare_per_ride",
    "adult_card_fare_per_ride",
    "senior_citizen_card_fare_per_ride",
    "student_card_fare_per_ride",
    "workfare_transport_concession_card_fare_per_ride",
    "persons_with_disabilities_card_fare_per_ride"
FROM "sg-data-d-bf2ed06b8fcda382b0f83133b174e07f"
