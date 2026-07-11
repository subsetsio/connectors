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
    CAST("SpontaneousVaginal" AS BIGINT) AS spontaneousvaginal,
    CAST("AssistedVaginal" AS BIGINT) AS assistedvaginal,
    CAST("CSectionAll" AS BIGINT) AS csectionall,
    CAST("CSectionElected" AS BIGINT) AS csectionelected,
    CAST("CSectionEmergency" AS BIGINT) AS csectionemergency,
    CAST("OtherNotKnown" AS BIGINT) AS othernotknown,
    CAST("PercentSpontaneousVaginal" AS DOUBLE) AS percentspontaneousvaginal,
    CAST("PercentAssistedVaginal" AS DOUBLE) AS percentassistedvaginal,
    CAST("PercentCSectionAll" AS DOUBLE) AS percentcsectionall,
    CAST("PercentCSectionElected" AS DOUBLE) AS percentcsectionelected,
    CAST("PercentCSectionEmergency" AS DOUBLE) AS percentcsectionemergency,
    CAST("PercentOtherNotKnown" AS DOUBLE) AS percentothernotknown,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    CAST("SIMDQuintile" AS BIGINT) AS simdquintile
FROM "public-health-scotland-covid-19-wider-impacts-method-of-delivery"
