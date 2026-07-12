-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "species_id",
    "species_name",
    "long_term_trend_percent",
    "long_term_slope",
    "long_term_slope_se",
    "ten_year_trend_percent",
    "ten_year_slope",
    "ten_year_slope_se",
    "habitat"
FROM "pecbms-species"
