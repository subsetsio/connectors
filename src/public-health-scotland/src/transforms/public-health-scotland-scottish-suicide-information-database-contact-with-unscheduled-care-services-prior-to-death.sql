-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "HealthcareService" AS healthcareservice,
    "TimeRange" AS timerange,
    "Country" AS country,
    "Age" AS age,
    "Sex" AS sex,
    "IndividualsCount" AS individualscount,
    "IndividualsCountQF" AS individualscountqf,
    "Deprivation" AS deprivation,
    "HBR" AS hbr,
    "CA" AS ca,
    "UCService" AS ucservice,
    CAST("CalendarYear" AS BIGINT) AS calendaryear,
    "ContactFrequency" AS contactfrequency
FROM "public-health-scotland-scottish-suicide-information-database-contact-with-unscheduled-care-services-prior-to-death"
