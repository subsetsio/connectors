-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_common_under_18_year_old_children",
    "place_of_residence_of_husband",
    "type_of_settlement_region",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv351u.px"
