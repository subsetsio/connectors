-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mother_s_socio_economic_status",
    "age_of_mother",
    "type_of_settlement_region",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv146u.px"
