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
    "la_name",
    "new_la_code",
    "pcon_code",
    "pcon_name",
    "phase_type_grouping",
    "establishment_type",
    "hospital_school",
    "sen_provision",
    "pupil_count",
    "pupil_percent"
FROM "dfe-019df85e-ab00-7458-a4ff-b381997776cb"
