-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "_name" AS name,
    "lat",
    "lon",
    "firstdata",
    "lastdata",
    "granularity",
    "travelmodes",
    "directional",
    "hastimestampeddata",
    "hasweather",
    "counters_id",
    "counters_serial",
    "counters_installationdate",
    "counters_detachmentdate",
    "domain_name"
FROM "nyc-open-data-6up2-gnw8"
