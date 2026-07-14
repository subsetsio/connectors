-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: City is not a city name and does not identify a row: it labels an urban area within one of the twelve US metropolitan regions the study covers (Downtown, Levittown, and similar), and the metropolitan region that would disambiguate it is absent from the table. Downtown therefore appears once per metro, and the rows cannot be told apart or joined to a place.
-- caution: City also carries 'Average' summary rows, which are study-wide aggregates rather than an urban area; exclude them before comparing places.
-- caution: Timeframe (Pre 1950 / Post 1950) marks the development era of the area's street network, not an observation date.
-- caution: Some rows carry no measurement at all; they are placeholders for an area the source listed but did not measure.
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
