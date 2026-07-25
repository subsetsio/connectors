-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "agency",
    "city",
    "state",
    "ntd_id",
    "organization_type",
    "reporter_type",
    CAST("report_year" AS BIGINT) AS report_year,
    "uace_code",
    "uza_name",
    CAST("primary_uza_population" AS BIGINT) AS primary_uza_population,
    CAST("agency_voms" AS BIGINT) AS agency_voms,
    CAST("fares" AS BIGINT) AS fares,
    "fares_questionable",
    CAST("park_and_ride" AS BIGINT) AS park_and_ride,
    "park_and_ride_questionable",
    CAST("concessions" AS BIGINT) AS concessions,
    "concessions_questionable",
    CAST("advertising" AS BIGINT) AS advertising,
    "advertising_questionable",
    CAST("other" AS BIGINT) AS other,
    "other_questionable",
    CAST("purchased_transportation" AS BIGINT) AS purchased_transportation,
    "purchased_transportation_1",
    CAST("total" AS BIGINT) AS total,
    "total_questionable"
FROM "u-s-department-of-transportation-yuaq-zdvc"
