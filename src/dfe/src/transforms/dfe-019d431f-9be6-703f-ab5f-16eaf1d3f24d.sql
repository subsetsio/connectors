-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("﻿time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "old_la_code",
    "la_name",
    "new_la_code",
    "social_care_group",
    "sen_provision",
    "sen_primary_need",
    "pupil_count",
    "pupil_percent"
FROM "dfe-019d431f-9be6-703f-ab5f-16eaf1d3f24d"
