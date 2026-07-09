-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Covers only the ~145 countries in the Atlas ranking universe (those flagged `in_rankings` in location-country), not all 233 locations — it is not a complete country panel.
-- caution: `growth_proj` is a forward-looking 10-year annualized GDP growth projection made as of that year, not an observed outcome, and it is only published for a subset of country-years.
-- caution: The three ECI variants (`eci_hs92`, `eci_hs12`, `eci_sitc`) are computed on different classifications over different year ranges, so their ranks are not comparable across columns and are null where that classification does not cover the year.
SELECT
    "country_id",
    "country_iso3_code",
    "year",
    "growth_proj",
    "in_rankings",
    "eci_sitc",
    "eci_rank_sitc",
    "eci_hs92",
    "eci_rank_hs92",
    "eci_hs12",
    "eci_rank_hs12"
FROM "harvard-growth-lab-atlas-of-economic-complexity-growth-proj-eci-rankings"
