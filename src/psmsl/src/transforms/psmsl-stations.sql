-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Station metadata is a reference catalog; join it to value tables by station_id rather than summing or counting it as observations.
SELECT
    "station_id",
    "latitude",
    "longitude",
    "station_name",
    "coastline_code",
    "station_code",
    "documentation_flag"
FROM "psmsl-stations"
