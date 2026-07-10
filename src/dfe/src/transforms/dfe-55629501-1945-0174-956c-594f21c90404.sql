-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "time_frame",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "new_la_code",
    "la_name",
    "old_la_code",
    strptime("reference_date", '%Y-%m-%d')::DATE AS reference_date,
    "education_phase",
    CAST("school_submitted_count" AS BIGINT) AS school_submitted_count,
    CAST("school_all_count" AS BIGINT) AS school_all_count
FROM "dfe-55629501-1945-0174-956c-594f21c90404"
