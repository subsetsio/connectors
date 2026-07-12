-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The location catalog includes countries, WDPA protected areas, and a worldwide aggregate, while the widget tables in this connector are scoped to countries plus worldwide.
SELECT
    "id",
    "location_uuid",
    "iso",
    "location_type",
    "name",
    "area_m2",
    "coast_length_m",
    "perimeter_m"
FROM "global-mangrove-watch-locations"
