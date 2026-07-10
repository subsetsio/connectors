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
    "version",
    "establistment_type_group",
    CAST("rwm_exp_pupil_percent" AS BIGINT) AS rwm_exp_pupil_percent,
    "establishment_count"
FROM "dfe-019afee5-c8fd-751d-b8b2-c31894a732af"
