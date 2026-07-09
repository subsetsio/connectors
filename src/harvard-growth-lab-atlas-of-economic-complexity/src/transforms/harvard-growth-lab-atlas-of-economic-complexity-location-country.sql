-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes non-sovereign territories and one former country (`former_country`) alongside sovereign states. `in_rankings` marks the subset that carries ECI ranks and growth projections; join on it before treating this as the analysis universe.
SELECT
    "country_id",
    "country_iso3_code",
    "country_name",
    "country_name_short",
    "in_rankings",
    "former_country"
FROM "harvard-growth-lab-atlas-of-economic-complexity-location-country"
