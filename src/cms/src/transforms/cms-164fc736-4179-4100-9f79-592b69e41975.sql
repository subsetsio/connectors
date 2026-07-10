-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "HCPCS_CD" AS hcpcs_cd,
    "HCPCS_INITIAL_MODIFIER_CD" AS hcpcs_initial_modifier_cd,
    "PROVIDER_SPEC_CD" AS provider_spec_cd,
    "CARRIER_NUM" AS carrier_num,
    "PRICING_LOCALITY_CD" AS pricing_locality_cd,
    "TYPE_OF_SERVICE_CD" AS type_of_service_cd,
    "PLACE_OF_SERVICE_CD" AS place_of_service_cd,
    "HCPCS_SECOND_MODIFIER_CD" AS hcpcs_second_modifier_cd,
    "PSPS_SUBMITTED_SERVICE_CNT" AS psps_submitted_service_cnt,
    "PSPS_SUBMITTED_CHARGE_AMT" AS psps_submitted_charge_amt,
    "PSPS_ALLOWED_CHARGE_AMT" AS psps_allowed_charge_amt,
    "PSPS_DENIED_SERVICES_CNT" AS psps_denied_services_cnt,
    "PSPS_DENIED_CHARGE_AMT" AS psps_denied_charge_amt,
    "PSPS_ASSIGNED_SERVICES_CNT" AS psps_assigned_services_cnt,
    CAST("PSPS_NCH_PAYMENT_AMT" AS DOUBLE) AS psps_nch_payment_amt,
    "PSPS_HCPCS_ASC_IND_CD" AS psps_hcpcs_asc_ind_cd,
    CAST("PSPS_ERROR_IND_CD" AS BIGINT) AS psps_error_ind_cd,
    "HCPCS_BETOS_CD" AS hcpcs_betos_cd
FROM "cms-164fc736-4179-4100-9f79-592b69e41975"
