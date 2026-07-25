-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "ntd_id",
    "agency_name",
    "city",
    "statecd",
    "reporter_type",
    CAST("agency_voms" AS BIGINT) AS agency_voms,
    "mode_name",
    "mode",
    "tos",
    CAST("mode_voms" AS BIGINT) AS mode_voms,
    "uace_code",
    "uza_name",
    "weblink",
    "alternate_format",
    CAST("waived" AS BOOLEAN) AS waived
FROM "u-s-department-of-transportation-venb-5asu"
