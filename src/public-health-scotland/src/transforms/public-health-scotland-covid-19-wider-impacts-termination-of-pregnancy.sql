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
    CAST("AverageGestation" AS DOUBLE) AS averagegestation,
    CAST("NumberTerminations" AS BIGINT) AS numberterminations,
    CAST("NumberGestation10to12Wks" AS BIGINT) AS numbergestation10to12wks,
    "NumberGestation10to12WksQF" AS numbergestation10to12wksqf,
    CAST("NumberGestationOver12Wks" AS BIGINT) AS numbergestationover12wks,
    "NumberGestationOver12WksQF" AS numbergestationover12wksqf,
    CAST("NumberGestationUnder10Wks" AS BIGINT) AS numbergestationunder10wks,
    "NumberGestationUnder10WksQF" AS numbergestationunder10wksqf,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile
FROM "public-health-scotland-covid-19-wider-impacts-termination-of-pregnancy"
