-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_power_plant",
    CAST("year" AS BIGINT) AS year,
    "indicator",
    "type_of_fuel_energy",
    "value"
FROM "statistics-estonia-ke033.px"
