-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "amenity_id",
    "amenity_type",
    "station_mrn",
    "station_name",
    "lines",
    "borough",
    "division",
    "latitude",
    "longitude",
    "original_install_date",
    "georeference"
FROM "mta-open-data-6yjv-fk7g"
