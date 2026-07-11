-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Renewal Funding Inflation Factor rows use HUD area definitions for voucher funding; do not treat the area code as a stable county-only key across years.
SELECT
    "fmr_area_code",
    "fmr_area_name",
    "fips2010",
    "county_town_name",
    "rfif",
    "fips2025",
    "fiscal_year"
FROM "hud-rfif"
