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
    "trust_name",
    CAST("trust_uid" AS BIGINT) AS trust_uid,
    "trust_id",
    CAST("trust_companies_house_number" AS BIGINT) AS trust_companies_house_number,
    CAST("trust_ukprn" AS BIGINT) AS trust_ukprn,
    "trust_leadregion",
    CAST("numinst_matptinc" AS BIGINT) AS numinst_matptinc,
    CAST("numinst_fsm6cla1a_matptinc" AS BIGINT) AS numinst_fsm6cla1a_matptinc,
    CAST("numinst_converter_matptinc" AS BIGINT) AS numinst_converter_matptinc,
    CAST("numinst_sponsor_matptinc" AS BIGINT) AS numinst_sponsor_matptinc,
    CAST("numinst_free_matptinc" AS BIGINT) AS numinst_free_matptinc,
    CAST("numinst_3_matptinc" AS BIGINT) AS numinst_3_matptinc,
    CAST("numinst_4plus_matptinc" AS BIGINT) AS numinst_4plus_matptinc,
    CAST("numinst_inmat" AS BIGINT) AS numinst_inmat,
    CAST("numinst_converter_inmat" AS BIGINT) AS numinst_converter_inmat,
    CAST("numinst_sponsor_inmat" AS BIGINT) AS numinst_sponsor_inmat,
    CAST("numinst_free_inmat" AS BIGINT) AS numinst_free_inmat
FROM "dfe-019b02dc-a9e9-7338-9500-0996ee82d91a"
