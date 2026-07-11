-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "HB" AS hb,
    "HBQF" AS hbqf,
    strptime("WeekBeginning", '%Y%m%d')::DATE AS weekbeginning,
    CAST("NumberWomenBooking" AS BIGINT) AS numberwomenbooking,
    CAST("NumberGestation10to12Wks" AS BIGINT) AS numbergestation10to12wks,
    CAST("NumberGestationOver12Wks" AS BIGINT) AS numbergestationover12wks,
    CAST("NumberGestationUnder10Wks" AS BIGINT) AS numbergestationunder10wks,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile
FROM "public-health-scotland-covid-19-wider-impacts-antenatal-bookings"
