-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "ACO_ID" AS aco_id,
    "State_Name" AS state_name,
    "County_Name" AS county_name,
    CAST("State_ID" AS BIGINT) AS state_id,
    CAST("County_ID" AS BIGINT) AS county_id,
    "AB_Psn_Yrs_ESRD" AS ab_psn_yrs_esrd,
    "AB_Psn_Yrs_DIS" AS ab_psn_yrs_dis,
    "AB_Psn_Yrs_AGDU" AS ab_psn_yrs_agdu,
    "AB_Psn_Yrs_AGND" AS ab_psn_yrs_agnd,
    "Tot_AB_Psn_Yrs" AS tot_ab_psn_yrs,
    "Tot_AB" AS tot_ab
FROM "cms-ae8c9418-acc9-4442-b217-33291448f6b8"
