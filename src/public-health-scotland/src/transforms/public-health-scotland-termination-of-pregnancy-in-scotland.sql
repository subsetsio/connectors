-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("YearofTermination" AS BIGINT) AS yearoftermination,
    "HBR" AS hbr,
    "ageGroup" AS agegroup,
    CAST("NumberofTerminations" AS BIGINT) AS numberofterminations,
    "TerminationQF" AS terminationqf,
    "EstimatedGestation" AS estimatedgestation,
    "SIMDQuintile" AS simdquintile,
    "SIMDVersion" AS simdversion,
    "TerminationMethod" AS terminationmethod,
    "Previous_Terminations" AS previous_terminations,
    "CA" AS ca,
    "Parity" AS parity
FROM "public-health-scotland-termination-of-pregnancy-in-scotland"
