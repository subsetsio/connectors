-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table combines two inequality measures in one long panel; filter or group by `measure` before comparing values or aggregating across countries and years.
SELECT
    "country_code",
    "country_alpha3",
    "country_name",
    "measure",
    "year",
    "value"
FROM "utip-ehii-ehii"
