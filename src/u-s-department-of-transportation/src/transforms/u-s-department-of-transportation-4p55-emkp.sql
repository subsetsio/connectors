-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "ntd_id",
    "reporter_name",
    "reporter_type_desc_short",
    "mode_code",
    "service_type_code",
    "day_name",
    "svc_begin_time",
    "svc_end_time",
    CAST("end_next_day_flag" AS BOOLEAN) AS end_next_day_flag,
    CAST("only_ada_flag" AS BOOLEAN) AS only_ada_flag,
    CAST("defined_by_agedisable" AS BOOLEAN) AS defined_by_agedisable,
    CAST("gen_population_flag" AS BOOLEAN) AS gen_population_flag
FROM "u-s-department-of-transportation-4p55-emkp"
