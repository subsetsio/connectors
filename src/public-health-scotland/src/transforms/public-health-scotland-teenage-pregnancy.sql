-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("YearOfConception" AS BIGINT) AS yearofconception,
    "CA" AS ca,
    CAST("Terminations" AS BIGINT) AS terminations,
    "TerminationsQF" AS terminationsqf,
    CAST("Deliveries" AS BIGINT) AS deliveries,
    "DeliveriesQF" AS deliveriesqf,
    CAST("Pregnancies" AS BIGINT) AS pregnancies,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    "AgeGroup" AS agegroup,
    "PregnanciesQF" AS pregnanciesqf,
    "SIMDQuintile1" AS simdquintile1,
    "SIMDQuintile1QF" AS simdquintile1qf,
    "SIMDQuintile2" AS simdquintile2,
    "SIMDQuintile2QF" AS simdquintile2qf,
    CAST("SIMDQuintile3" AS BIGINT) AS simdquintile3,
    "SIMDQuintile3QF" AS simdquintile3qf,
    "SIMDQuintile4" AS simdquintile4,
    "SIMDQuintile4QF" AS simdquintile4qf,
    "SIMDQuintile5" AS simdquintile5,
    "SIMDQuintile5QF" AS simdquintile5qf,
    "SIMDVersion" AS simdversion,
    "Outcome" AS outcome
FROM "public-health-scotland-teenage-pregnancy"
