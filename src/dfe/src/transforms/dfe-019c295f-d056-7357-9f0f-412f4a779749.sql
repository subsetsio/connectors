-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("﻿""time_period""" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "version",
    "trust_name",
    "trust_id",
    CAST("trust_uid" AS BIGINT) AS trust_uid,
    CAST("trust_companies_house_number" AS BIGINT) AS trust_companies_house_number,
    CAST("trust_ukprn" AS BIGINT) AS trust_ukprn,
    "trust_lead_region",
    "performance_tables_eligibility",
    "urns_in_mat",
    "exam_cohort",
    CAST("academy_count" AS BIGINT) AS academy_count,
    CAST("converter_count" AS BIGINT) AS converter_count,
    CAST("sponsor_count" AS BIGINT) AS sponsor_count,
    CAST("free_count" AS BIGINT) AS free_count,
    CAST("utc_count" AS BIGINT) AS utc_count,
    CAST("studio_count" AS BIGINT) AS studio_count,
    "years_3_count",
    "years_4_count",
    "years_5plus_count"
FROM "dfe-019c295f-d056-7357-9f0f-412f4a779749"
