-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "medallion_number",
    "_1st_inspection_dmv_facility_inspection_month" AS 1st_inspection_dmv_facility_inspection_month,
    "_2nd_inspection_scheduled_date" AS 2nd_inspection_scheduled_date,
    "_2nd_inspection_scheduled_time" AS 2nd_inspection_scheduled_time,
    "_3rd_inspection_scheduled_date" AS 3rd_inspection_scheduled_date,
    "_3rd_inspection_scheduled_time" AS 3rd_inspection_scheduled_time,
    "fleetagentcode",
    "agentname",
    "last_updated_date_time"
FROM "nyc-open-data-sp7n-275u"
