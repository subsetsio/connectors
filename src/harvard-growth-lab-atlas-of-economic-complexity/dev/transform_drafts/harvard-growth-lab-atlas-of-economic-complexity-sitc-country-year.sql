-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `growth_proj` is a forward-looking 10-year annualized GDP growth projection made as of that year, not an observed outcome, and it is only published for a subset of country-years.
SELECT
    "country_id",
    "country_iso3_code",
    "year",
    "export_value",
    "import_value",
    "eci",
    "coi",
    "diversity",
    "growth_proj"
FROM "harvard-growth-lab-atlas-of-economic-complexity-sitc-country-year"
