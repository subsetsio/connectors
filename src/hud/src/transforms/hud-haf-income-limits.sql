-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Homeowner Assistance Fund income-limit rows are eligibility-area records, not a purely county-level geography.
SELECT
    "fips2010",
    "state",
    CAST("county" AS BIGINT) AS county,
    "areaname",
    "county_name",
    "county_town_name",
    "cbsasub",
    "median",
    "haf100_p1",
    "haf100_p2",
    "haf100_p3",
    "haf100_p4",
    "haf100_p5",
    "haf100_p6",
    "haf100_p7",
    "haf100_p8",
    "haf150_p1",
    "haf150_p2",
    "haf150_p3",
    "haf150_p4",
    "haf150_p5",
    "haf150_p6",
    "haf150_p7",
    "haf150_p8",
    "fips",
    "fiscal_year"
FROM "hud-haf-income-limits"
