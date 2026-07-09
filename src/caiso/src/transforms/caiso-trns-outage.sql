-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Transmission outage rows describe events with planned and actual timing; use outage start and end columns instead of treating every row as a uniform interval observation.
SELECT
    "TI_ID" AS ti_id,
    "TI_DIRECTION" AS ti_direction,
    "EQUIPMENT_OUTAGE" AS equipment_outage,
    "OUTAGE_NOTES" AS outage_notes,
    "AUDIT_TYPE" AS audit_type,
    "START_DATE" AS start_date,
    "END_DATE" AS end_date,
    "START_HOUR" AS start_hour,
    "END_HOUR" AS end_hour,
    "CURTAILED_OTC_MW" AS curtailed_otc_mw,
    "UPD_DATE" AS upd_date,
    "UPD_DATE_GMT" AS upd_date_gmt,
    "UPD_BY" AS upd_by,
    "OASIS_REC_STAT" AS oasis_rec_stat,
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt
FROM "caiso-trns-outage"
