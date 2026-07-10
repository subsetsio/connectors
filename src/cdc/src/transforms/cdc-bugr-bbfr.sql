-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "provider_location_guid",
    "loc_store_no",
    "loc_phone",
    "loc_name",
    "loc_admin_street1",
    "loc_admin_street2",
    "loc_admin_city",
    "loc_admin_state",
    "loc_admin_zip",
    "sunday_hours",
    "monday_hours",
    "tuesday_hours",
    "wednesday_hours",
    "thursday_hours",
    "friday_hours",
    "saturday_hours",
    "web_address",
    "pre_screen",
    CAST("insurance_accepted" AS BOOLEAN) AS insurance_accepted,
    CAST("walkins_accepted" AS BOOLEAN) AS walkins_accepted,
    "provider_notes",
    "searchable_name",
    CAST("in_stock" AS BOOLEAN) AS in_stock,
    CAST("supply_level" AS BIGINT) AS supply_level,
    strptime("quantity_last_updated", '%Y-%m-%d')::DATE AS quantity_last_updated,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "category"
FROM "cdc-bugr-bbfr"
