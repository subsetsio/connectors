-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ntd_id",
    "legacy_ntd_id",
    "agency",
    "mode_type_of_service_status",
    "reporter_type",
    "uace_cd",
    "uza_name",
    "mode",
    "tos",
    "_3_mode" AS 3_mode,
    CAST("date" AS TIMESTAMP) AS date,
    CAST("upt" AS BIGINT) AS upt,
    CAST("voms" AS BIGINT) AS voms,
    CAST("vrh" AS BIGINT) AS vrh,
    CAST("vrm" AS BIGINT) AS vrm,
    "agency_mode_tos_date",
    "state",
    CAST("fta_region" AS BIGINT) AS fta_region
FROM "u-s-department-of-transportation-8bui-9xvu"
