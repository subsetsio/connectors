-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "segmentid",
    "complexid",
    "saftype",
    "placeid",
    "bin",
    "_source" AS source,
    "objectid",
    "sos_indicator",
    "facility_domains",
    "borough_code",
    "source_id",
    "created_by",
    "created_date",
    "modified_by",
    "modified_date",
    "facility_type",
    "b7sc",
    "primary_address_point_id",
    "feature_name",
    "security_level"
FROM "nyc-open-data-t95h-5fsr"
