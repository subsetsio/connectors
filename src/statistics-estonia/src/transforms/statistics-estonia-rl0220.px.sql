-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_of_construction",
    "occupancy",
    "comfort_characteristics",
    "number_of_rooms",
    "county",
    "value"
FROM "statistics-estonia-rl0220.px"
