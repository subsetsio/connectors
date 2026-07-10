-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Boundary reference table carries ArcGIS geometry-derived area and length fields; use the identifier columns for joins rather than treating geometry measures as statistical observations.
SELECT
    "OBJECTID" AS objectid,
    "geoid",
    "fips_code",
    "county_name",
    "juris_name",
    "CountyFP" AS countyfp,
    "CountySort" AS countysort,
    "CitySort" AS citysort,
    "CityShort" AS cityshort
FROM "california-department-of-finance-0f2f9e220e3b4ebc890e2a178560e574"
