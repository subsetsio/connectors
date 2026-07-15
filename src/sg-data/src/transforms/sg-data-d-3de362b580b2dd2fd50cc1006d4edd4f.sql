-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "avg_opt_margin_kgco2-per-kwh" AS avg_opt_margin_kgco2_per_kwh,
    "build_margin_kgco2-per-kwh" AS build_margin_kgco2_per_kwh,
    "upstream_fugitive_methane_emission_factor_kgch4-per-kwh" AS upstream_fugitive_methane_emission_factor_kgch4_per_kwh
FROM "sg-data-d-3de362b580b2dd2fd50cc1006d4edd4f"
