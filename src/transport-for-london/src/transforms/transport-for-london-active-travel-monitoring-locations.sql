-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The reference table can contain multiple rows per site_id where site metadata or location descriptors differ; join to counts with awareness that site_id alone is not declared as the table grain.
SELECT
    "site_id",
    "location_description",
    "borough",
    "functional_area",
    "road_type",
    CAST("strategic_cio_panel" AS BIGINT) AS strategic_cio_panel,
    "old_site_id",
    CAST("easting" AS BIGINT) AS easting,
    CAST("northing" AS BIGINT) AS northing,
    "latitude",
    CAST("longitude" AS DOUBLE) AS longitude
FROM "transport-for-london-active-travel-monitoring-locations"
