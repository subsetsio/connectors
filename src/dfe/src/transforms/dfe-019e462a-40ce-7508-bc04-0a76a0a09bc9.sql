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
    "region_code",
    "region_name",
    "fe_sector_type",
    "provider_type",
    "main_role_type",
    "contract_type",
    "characteristic",
    "characteristic_type",
    "number_staff_fte",
    CAST("number_staff_hc" AS BIGINT) AS number_staff_hc,
    "perc_fte",
    "perc_hc"
FROM "dfe-019e462a-40ce-7508-bc04-0a76a0a09bc9"
