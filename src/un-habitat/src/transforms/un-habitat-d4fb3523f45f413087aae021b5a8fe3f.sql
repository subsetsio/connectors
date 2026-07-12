-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is specific to United States cities; do not combine it with global street-density tables without harmonizing geography and metric definitions.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "City" AS city,
    "Pct_Proportion_of_land_Allocate" AS pct_proportion_of_land_allocate,
    "Street_density__Km_per_Km2" AS street_density_km_per_km2,
    "Intersection_density_No_per_Km2" AS intersection_density_no_per_km2,
    "Timeframe" AS timeframe,
    "ObjectId" AS objectid
FROM "un-habitat-d4fb3523f45f413087aae021b5a8fe3f"
