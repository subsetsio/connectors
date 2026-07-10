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
    "establishment_type_group",
    "sex",
    "mtc_score",
    CAST("pupil_count" AS BIGINT) AS pupil_count,
    CAST("cumulative_pupil_count" AS BIGINT) AS cumulative_pupil_count,
    CAST("cumulative_pupil_percent" AS BIGINT) AS cumulative_pupil_percent
FROM "dfe-019a838d-feb1-76e7-8fda-77f0ae44e73f"
