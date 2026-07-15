-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Owner_Occupied" AS owner_occupied,
    "Rented" AS rented,
    "Others" AS others
FROM "sg-data-d-1ca435a3b62aafa6857d96368971765b"
