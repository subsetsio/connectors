-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "facility_name",
    "facility_id",
    "facility_owner_dsny_or_private",
    "facility_type",
    "facility_contracted_tons_per_day",
    "facility_avg_delivered_tons_per_day",
    "facility_actual_tons_delivered_per_year",
    "facility_price_per_ton",
    "facility_total_loads"
FROM "nyc-open-data-6r9j-qrwz"
