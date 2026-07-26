-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("permit_num" AS BIGINT) AS permit_num,
    "vas_org",
    "prim_territory",
    CAST("dot_id" AS BIGINT) AS dot_id,
    CAST("veh_hrs_from" AS BIGINT) AS veh_hrs_from,
    "veh_hrs_from_ampm",
    CAST("veh_hrs_to" AS BIGINT) AS veh_hrs_to,
    "veh_hrs_to_ampm",
    "sun",
    "mon",
    "tue",
    "wed",
    "thur",
    "fri",
    "sat",
    strptime("permit_effective_date", '%m/%d/%Y')::DATE AS permit_effective_date,
    strptime("permit_expiration_date", '%m/%d/%Y')::DATE AS permit_expiration_date,
    strptime("permit_issued_date", '%m/%d/%Y')::DATE AS permit_issued_date,
    "permit_status",
    "plate_state",
    "lost_app_vehicle_stolen",
    strptime("appl_date", '%m/%d/%Y')::DATE AS appl_date,
    "appl_status",
    "appl_definition",
    "city",
    "cust_state",
    CAST("zip" AS BIGINT) AS zip
FROM "nyc-open-data-ue2f-z6i6"
