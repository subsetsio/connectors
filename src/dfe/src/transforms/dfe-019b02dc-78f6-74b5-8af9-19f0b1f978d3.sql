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
    "trust_name",
    CAST("trust_uid" AS BIGINT) AS trust_uid,
    "trust_id",
    CAST("trust_companies_house_number" AS BIGINT) AS trust_companies_house_number,
    CAST("trust_ukprn" AS BIGINT) AS trust_ukprn,
    "trust_leadregion",
    "institutions_matptinc",
    "disadvantage_status",
    "eligible_pupil_count",
    "rwm_exp_wgtavg_percent"
FROM "dfe-019b02dc-78f6-74b5-8af9-19f0b1f978d3"
