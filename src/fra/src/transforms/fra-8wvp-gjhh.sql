-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This six-year view is a windowed view of the operational Form 55 data and should not be added to the full operational tables without de-duplication.
SELECT
    "railroadcode",
    "railroadname",
    "reportmonth",
    CAST("year" AS BIGINT) AS year,
    "statecode",
    "statename",
    CAST("countycode" AS BIGINT) AS countycode,
    "countyname",
    CAST("freighttrainmiles" AS BIGINT) AS freighttrainmiles,
    CAST("passengertrainmiles" AS BIGINT) AS passengertrainmiles,
    CAST("yardswitchingmiles" AS BIGINT) AS yardswitchingmiles,
    CAST("othertrainmiles" AS BIGINT) AS othertrainmiles,
    CAST("totalmiles" AS BIGINT) AS totalmiles,
    CAST("employeemanhours" AS BIGINT) AS employeemanhours,
    CAST("passengermiles" AS BIGINT) AS passengermiles,
    CAST("passengerstransported" AS BIGINT) AS passengerstransported,
    CAST("locomotivetrainmiles" AS BIGINT) AS locomotivetrainmiles,
    CAST("motortrainmiles" AS BIGINT) AS motortrainmiles,
    "railroadtype",
    CAST("district" AS BIGINT) AS district,
    "narrative",
    "reporting_railroad_smt_grouping",
    "reporting_railroad_class",
    "reporting_parent_railroad_code",
    "reporting_parent_railroad_name",
    "reporting_railroad_holding_company",
    "reporting_railroad_individual_class",
    "reporting_railroad_passenger",
    "reporting_railroad_commuter",
    "reporting_railroad_switching_terminal",
    "reporting_railroad_tourist",
    "reporting_railroad_freight",
    "reporting_railroad_short_line",
    "reportkey"
FROM "fra-8wvp-gjhh"
