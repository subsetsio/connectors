-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `ANS` (`country_id` 999, "Undeclared Countries") is a residual bucket for unattributable trade rather than a real location, and `ANT` (Netherlands Antilles) is a dissolved country retained for historical years — both sit alongside the sovereign states and territories.
-- caution: `in_rankings` marks the subset of countries that carry ECI ranks and growth projections; join on it before treating this table as the analysis universe.
SELECT
    "country_id",
    "country_iso3_code",
    "country_name",
    "country_name_short",
    "in_rankings",
    "former_country"
FROM "harvard-growth-lab-atlas-of-economic-complexity-location-country"
