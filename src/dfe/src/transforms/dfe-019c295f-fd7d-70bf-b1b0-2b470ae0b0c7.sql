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
    "exam_cohort",
    "disadvantage_status",
    "students_in_mat_count",
    "eligible_students_count",
    "aps_per_entry",
    "aps_per_entry_grade",
    "points_sum",
    "entries_count",
    "disadvantaged_percent",
    "value_added",
    "value_added_lower_ci",
    "value_added_upper_ci",
    "progress_banding"
FROM "dfe-019c295f-fd7d-70bf-b1b0-2b470ae0b0c7"
