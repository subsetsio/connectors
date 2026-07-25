-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date" AS TIMESTAMP) AS date,
    CAST("combined_tsi" AS DOUBLE) AS combined_tsi,
    CAST("freight_tsi" AS DOUBLE) AS freight_tsi,
    CAST("passenger_tsi" AS DOUBLE) AS passenger_tsi
FROM "u-s-department-of-transportation-3w2s-iysp"
