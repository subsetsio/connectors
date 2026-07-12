-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "pollutant",
    "lmlwth",
    "clean",
    "normal",
    "less_than_normal",
    "limited_polluted",
    "polluted",
    "extremely_polluted",
    "total"
FROM "qatar-planning-and-statistics-authority-daily-percentages-of-air-quality-indicators-aspire-zone"
