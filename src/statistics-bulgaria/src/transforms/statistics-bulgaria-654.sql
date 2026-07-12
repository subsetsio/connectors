-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("period" AS BIGINT) AS period,
    "type_of_buildings",
    "type_of_buildings_2",
    "district",
    "periods",
    "value"
FROM "statistics-bulgaria-654"
