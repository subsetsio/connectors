-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "version",
    CAST("school_urn" AS BIGINT) AS school_urn,
    "school_name",
    "address",
    "postcode",
    "phone_number",
    "religious_denomination",
    "admissions_policy",
    "sex_policy",
    "age_range",
    CAST("school_laestab" AS BIGINT) AS school_laestab,
    "establishment_type",
    CAST("old_la_code" AS BIGINT) AS old_la_code,
    "new_la_code",
    "la_name",
    "pcon_code",
    "pcon_name",
    "lad_code",
    "lad_name",
    "rurality_code",
    "rurality_name",
    "region_code",
    "region_name",
    "country_code",
    "country_name"
FROM "dfe-019c2960-34d9-71c0-976c-3540602f2669"
