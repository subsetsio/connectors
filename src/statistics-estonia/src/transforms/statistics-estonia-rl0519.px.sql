-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "socio_economic_status",
    "indicator",
    "time_of_immigration_return",
    "age_group",
    "county",
    "sex",
    "value"
FROM "statistics-estonia-rl0519.px"
