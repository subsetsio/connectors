-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `iso3` field contains both country ISO3 codes and source-specific subnational/admin-unit codes; filter or join with category_type before treating rows as countries.
SELECT
    "continent",
    "category_type",
    "admin_level",
    "category_info",
    "income_value",
    "notes",
    "iso3",
    "country_name",
    "iso_group"
FROM "inform-countries"
