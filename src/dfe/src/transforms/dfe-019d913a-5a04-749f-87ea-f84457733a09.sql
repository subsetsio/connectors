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
    "exam_cohort",
    "x_range",
    CAST("x_midpoint" AS BIGINT) AS x_midpoint,
    CAST("xmin" AS BIGINT) AS xmin,
    CAST("xmax" AS BIGINT) AS xmax,
    CAST("count" AS BIGINT) AS count
FROM "dfe-019d913a-5a04-749f-87ea-f84457733a09"
