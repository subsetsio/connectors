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
    CAST("Month" AS BIGINT) AS month,
    CAST("AllBirths" AS BIGINT) AS allbirths,
    CAST("Gestation32to36Wks" AS BIGINT) AS gestation32to36wks,
    CAST("Gestation37to41Wks" AS BIGINT) AS gestation37to41wks,
    CAST("Gestation42WksOrOver" AS BIGINT) AS gestation42wksorover,
    CAST("GestationUnder32Wks" AS BIGINT) AS gestationunder32wks,
    CAST("GestationUnder37Wks" AS BIGINT) AS gestationunder37wks,
    CAST("Gestation18to44Wks" AS BIGINT) AS gestation18to44wks,
    CAST("GestationUnknown" AS BIGINT) AS gestationunknown,
    CAST("Percent32to36Wks" AS DOUBLE) AS percent32to36wks,
    CAST("Percent37to41Wks" AS DOUBLE) AS percent37to41wks,
    CAST("Percent42WksOrOver" AS DOUBLE) AS percent42wksorover,
    CAST("PercentUnder32Wks" AS DOUBLE) AS percentunder32wks,
    CAST("PercentUnder37Wks" AS DOUBLE) AS percentunder37wks,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile
FROM "public-health-scotland-covid-19-wider-impacts-gestation-at-delivery"
