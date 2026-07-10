-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_name",
    "region_code",
    "old_la_code",
    "new_la_code",
    "la_name",
    "pcon_code",
    "pcon_name",
    "phase_type_grouping",
    "fsm_eligibility",
    "fsm_breakdown",
    CAST("pupil_count" AS BIGINT) AS pupil_count,
    CAST("pupil_percent" AS DOUBLE) AS pupil_percent
FROM "dfe-019e7404-df19-71ce-90a8-f2e3db7dd7fa"
