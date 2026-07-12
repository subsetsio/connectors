-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_of_construction",
    "occupancy",
    "comfort_characteristics",
    "number_of_rooms",
    "location",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rl21220.px"
